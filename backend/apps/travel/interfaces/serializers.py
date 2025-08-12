from rest_framework import serializers
from ..models import TravelRequest, Traveler, TIPO_TRANSPORTE, MEIO_TRANSPORTE
from ..domain.value_objects import DateRange, CPF, BankAccount, Money, DailyAllowance
from ..domain.entities import Traveler as TravelerEntity, TravelRequest as TravelRequestEntity
from travel.utils.encryption import encrypt_data, decrypt_data

class DiariasCalculatorSerializer(serializers.Serializer):
    start_date = serializers.DateField(input_formats=["%Y-%m-%d"])
    end_date = serializers.DateField(input_formats=["%Y-%m-%d"])
    role = serializers.CharField(max_length=100)
    cds = serializers.CharField(max_length=100, required=False, allow_blank=True)
    fora_do_estado = serializers.BooleanField(default=False)
    via_aerea = serializers.BooleanField(default=False)
    exige_pernoite = serializers.BooleanField(default=True)

    def validate(self, data):
        start_date = data['start_date']
        end_date = data['end_date']
        try:
            data['travel_period'] = DateRange(start_date, end_date)
        except (ValueError, TypeError) as e:
            raise serializers.ValidationError(str(e))
        return data

class CPFField(serializers.Field):
    def to_internal_value(self, data):
        try:
            return CPF(data)
        except (ValueError, TypeError) as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, value):
        return str(value)

class TravelerSerializer(serializers.ModelSerializer):
    cpf = CPFField()

    class Meta:
        model = Traveler
        fields = ['id', 'nome', 'matricula', 'cargo', 'cds', 'cpf', 'banco', 'agencia', 'conta_corrente', 'valor_unitario', 'qtd_diarias', 'valor_total', 'tipo']
        read_only_fields = ['valor_unitario', 'qtd_diarias', 'valor_total']

    def validate(self, data):
        # Valida e cria o Value Object BankAccount
        try:
            BankAccount(
                agency=data.get('agencia'),
                account_number=data.get('conta_corrente'),
                bank_name=data.get('banco')
            )
        except (ValueError, TypeError, KeyError) as e:
            raise serializers.ValidationError({'bank_account': f"Dados bancários inválidos: {e}"})
        return data

    def create(self, validated_data):
        # O CPF já é um VO, mas o modelo espera string
        validated_data['cpf'] = validated_data['cpf'].value
        # Criptografa os dados bancários antes de salvar
        validated_data['banco'] = encrypt_data(validated_data['banco'])
        validated_data['agencia'] = encrypt_data(validated_data['agencia'])
        validated_data['conta_corrente'] = encrypt_data(validated_data['conta_corrente'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # O CPF já é um VO, mas o modelo espera string
        if 'cpf' in validated_data:
            validated_data['cpf'] = validated_data['cpf'].value
        # Criptografa os dados bancários antes de atualizar
        if 'banco' in validated_data:
            validated_data['banco'] = encrypt_data(validated_data['banco'])
        if 'agencia' in validated_data:
            validated_data['agencia'] = encrypt_data(validated_data['agencia'])
        if 'conta_corrente' in validated_data:
            validated_data['conta_corrente'] = encrypt_data(validated_data['conta_corrente'])
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Descriptografa os dados bancários ao ler
        representation['banco'] = decrypt_data(instance.banco)
        representation['agencia'] = decrypt_data(instance.agencia)
        representation['conta_corrente'] = decrypt_data(instance.conta_corrente)
        return representation

class TravelRequestSerializer(serializers.ModelSerializer):
    travelers = TravelerSerializer(many=True)

    class Meta:
        model = TravelRequest
        fields = ['id', 'unidade_orcamentaria', 'orgao_solicitante', 'justificativa', 'objetivo', 'itinerario', 'data_ida', 'data_retorno', 'transporte_tipo', 'transporte_meio', 'descricao_veiculo', 'criado_por', 'data_criacao', 'travelers']
        read_only_fields = ['data_criacao']

    def create(self, validated_data):
        travelers_data = validated_data.pop('travelers')
        travel_request = TravelRequest.objects.create(**validated_data)
        for traveler_data in travelers_data:
            Traveler.objects.create(travel=travel_request, **traveler_data)
        return travel_request

    def update(self, instance, validated_data):
        travelers_data = validated_data.pop('travelers')
        travelers = (instance.travelers).all()
        travelers_map = {traveler.id: traveler for traveler in travelers}

        instance.unidade_orcamentaria = validated_data.get('unidade_orcamentaria', instance.unidade_orcamentaria)
        instance.orgao_solicitante = validated_data.get('orgao_solicitante', instance.orgao_solicitante)
        instance.justificativa = validated_data.get('justificativa', instance.justificativa)
        instance.objetivo = validated_data.get('objetivo', instance.objetivo)
        instance.itinerario = validated_data.get('itinerario', instance.itinerario)
        instance.data_ida = validated_data.get('data_ida', instance.data_ida)
        instance.data_retorno = validated_data.get('data_retorno', instance.data_retorno)
        instance.transporte_tipo = validated_data.get('transporte_tipo', instance.transporte_tipo)
        instance.transporte_meio = validated_data.get('transporte_meio', instance.transporte_meio)
        instance.descricao_veiculo = validated_data.get('descricao_veiculo', instance.descricao_veiculo)
        instance.criado_por = validated_data.get('criado_por', instance.criado_por)
        instance.save()

        # Update or create travelers
        for traveler_data in travelers_data:
            traveler_id = traveler_data.get('id')
            if traveler_id and traveler_id in travelers_map:
                traveler = travelers_map.pop(traveler_id)
                for attr, value in traveler_data.items():
                    if attr == 'cpf':
                        setattr(traveler, attr, value.value)
                    else:
                        setattr(traveler, attr, value)
                traveler.save()
            else:
                Traveler.objects.create(travel=instance, **traveler_data)

        # Delete removed travelers
        for traveler in travelers_map.values():
            traveler.delete()

        return instance
