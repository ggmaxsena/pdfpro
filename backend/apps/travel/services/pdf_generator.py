from django.template.loader import render_to_string
# from weasyprint import HTML

class PdfGeneratorService:
    def generate_travel_request_pdf(self, travel_request_data: dict) -> bytes:
        # html_string = render_to_string('pdf/travel_request.html', {'travel_request': travel_request_data})
        # html = HTML(string=html_string)
        # pdf = html.write_pdf()
        # return pdf
        return b"PDF generation temporarily disabled."
