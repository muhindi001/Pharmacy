from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

class PDFReportGenerator:

    @staticmethod
    def generate(title, headers, rows):

        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(title, styles["Heading1"])
        )

        elements.append(Spacer(1, 12))

        table_data = [headers]

        table_data.extend(rows)

        table = Table(table_data)

        table.setStyle(

            TableStyle(

                [

                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

                    ("GRID", (0, 0), (-1, -1), 1, colors.black),

                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                    ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ]

            )

        )

        elements.append(table)

        document.build(elements)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf