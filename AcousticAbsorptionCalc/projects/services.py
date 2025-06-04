import csv
import tempfile

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
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


class CSVExportService:
    @staticmethod
    def generate_project_csv(project):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="project_{project.id}.csv"'
        )

        writer = csv.writer(response)

        writer.writerow(
            [
                _("Room Name"),
                _("Area (m²)"),
                _("Created At"),
            ]
        )

        for room in project.rooms.all():
            writer.writerow(
                [
                    room.name,
                    room.area,
                    room.created_at.strftime("%Y-%m-%d %H:%M"),
                ]
            )

        return response
