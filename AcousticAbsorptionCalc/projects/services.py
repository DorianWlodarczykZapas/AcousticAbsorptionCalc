import tempfile

from django.template.loader import render_to_string
from weasyprint import HTML


class PDFGeneratorService:
    @staticmethod
    def generate_project_pdf(context: dict) -> bytes:
        html_string = render_to_string("projects/pdf/project_detail_pdf.html", context)
        html = HTML(string=html_string)

        with tempfile.NamedTemporaryFile(suffix=".pdf") as pdf_file:
            html.write_pdf(target=pdf_file.name)
            pdf_file.seek(0)
            return pdf_file.read()
