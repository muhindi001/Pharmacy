import csv
import io

import pandas as pd
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .models import Medicine


def import_medicines(file):
    if not file:
        return 0, 0

    if file.name.endswith(".csv"):
        dataframe = pd.read_csv(file)
    else:
        dataframe = pd.read_excel(file)

    imported = 0
    updated = 0

    for _, row in dataframe.iterrows():
        medicine, created = Medicine.objects.update_or_create(
            barcode=row["barcode"],
            defaults={
                "medicine_name": row["medicine_name"],
                "generic_name": row["generic_name"],
                "sku": row["sku"],
                "buying_price": row["buying_price"],
                "selling_price": row["selling_price"],
                "unit": row["unit"],
                "qty": row["qty"],
                "expiry_date": row["expiry_date"],
                "prescription_required": row["prescription_required"],
                "controlled_drug": row["controlled_drug"],
            },
        )

        if created:
            imported += 1
        else:
            updated += 1

    return imported, updated


def export_csv():
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="medicines.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Medicine",
        "Generic",
        "Barcode",
        "SKU",
        "Buying Price",
        "Selling Price",
        "Quantity",
    ])

    for medicine in Medicine.objects.all():
        writer.writerow([
            medicine.medicine_name,
            medicine.generic_name,
            medicine.barcode,
            medicine.sku,
            medicine.buying_price,
            medicine.selling_price,
            medicine.qty,
        ])

    return response


def export_excel():
    output = io.BytesIO()
    dataframe = pd.DataFrame([
        {
            "Medicine": medicine.medicine_name,
            "Generic": medicine.generic_name,
            "Barcode": medicine.barcode,
            "SKU": medicine.sku,
            "Buying Price": medicine.buying_price,
            "Selling Price": medicine.selling_price,
            "Quantity": medicine.qty,
        }
        for medicine in Medicine.objects.all()
    ])

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Medicines")

    response = HttpResponse(output.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="medicines.xlsx"'
    return response


def export_pdf():
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="medicines.pdf"'

    document = SimpleDocTemplate(response, pagesize=letter)
    data = [[
        "Medicine",
        "Generic",
        "Barcode",
        "Qty",
        "Selling Price",
    ]]

    for medicine in Medicine.objects.all():
        data.append([
            medicine.medicine_name,
            medicine.generic_name,
            medicine.barcode,
            medicine.qty,
            medicine.selling_price,
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    document.build([table])

    return response
