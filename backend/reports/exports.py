import csv
from io import StringIO

from django.http import HttpResponse

from .excel import ExcelReportGenerator
from .pdf import PDFReportGenerator


class ReportExportService:
    """
    Generic export service for PDF, Excel and CSV reports.
    """

    @staticmethod
    def export_pdf(title, headers, rows, filename):

        pdf = PDFReportGenerator.generate(
            title=title,
            headers=headers,
            rows=rows,
        )

        response = HttpResponse(
            pdf,
            content_type="application/pdf",
        )

        response[
            "Content-Disposition"
        ] = f'attachment; filename="{filename}.pdf"'

        return response

    @staticmethod
    def export_excel(title, headers, rows, filename):

        excel = ExcelReportGenerator.generate(
            title=title,
            headers=headers,
            rows=rows,
        )

        response = HttpResponse(
            excel,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response[
            "Content-Disposition"
        ] = f'attachment; filename="{filename}.xlsx"'

        return response

    @staticmethod
    def export_csv(headers, rows, filename):

        buffer = StringIO()

        writer = csv.writer(buffer)

        writer.writerow(headers)

        for row in rows:
            writer.writerow(row)

        response = HttpResponse(
            buffer.getvalue(),
            content_type="text/csv",
        )

        response[
            "Content-Disposition"
        ] = f'attachment; filename="{filename}.csv"'

        return response