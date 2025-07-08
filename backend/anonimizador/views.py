
import pandas as pd
import re
from io import BytesIO
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import AnonimizationLog

def anonymize_cpf(cpf):
    return f'XXX.{cpf[3:6]}.{cpf[6:9]}-XX'

def anonymize_rg(rg):
    return f'XX{rg[2:-2]}XX'

def anonymize_name(name):
    parts = name.split()
    if len(parts) > 1:
        return f'{parts[0]} {". ".join([p[0] for p in parts[1:-1]])}. {parts[-1][0]}.'
    return name

class AnonymizeView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        xls = pd.ExcelFile(file_obj, engine='openpyxl')
        output = BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                for col in df.columns:
                    # Anonymize by column name
                    if 'cpf' in col.lower():
                        df[col] = df[col].astype(str).apply(anonymize_cpf)
                    elif 'rg' in col.lower():
                        df[col] = df[col].astype(str).apply(anonymize_rg)
                    elif 'nome' in col.lower():
                        df[col] = df[col].astype(str).apply(anonymize_name)
                    elif 'processo' in col.lower():
                        df[col] = 'Não informado'
                    else:
                        # Anonymize by content
                        df[col] = df[col].astype(str).apply(lambda x: 
                            anonymize_cpf(x) if re.match(r'^\d{11}$', x) else
                            anonymize_rg(x) if re.match(r'^\d{6,9}$', x) and not re.match(r'^\d{11}$', x) and not re.match(r'^\d{14}$', x) else
                            anonymize_name(x) if re.match(r'^[A-Za-z\s]+$', x) and len(x.split()) > 1 else
                            'Não informado' if re.match(r'^\d{16}$', x) else x
                        )
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        output.seek(0)

        AnonimizationLog.objects.create(
            user=request.user,
            file_name=file_obj.name,
            sheet_names=xls.sheet_names
        )

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=anonimized_{file_obj.name}'
        return response
