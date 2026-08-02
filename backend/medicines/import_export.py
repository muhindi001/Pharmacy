import csv
import io
from decimal import Decimal, InvalidOperation

import pandas as pd
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from categories.models import Category
from manufacturers.models import Manufacturer

from .models import Medicine


def _normalize_key(value):
    return str(value).strip().lower().replace(" ", "_").replace("-", "_").replace("/", "_")


def _get_first_value(row, *keys):
    normalized = {_normalize_key(k): v for k, v in row.items()}
    for key in keys:
        value = normalized.get(_normalize_key(key))
        if value not in (None, ""):
            return value
    return None


def _parse_decimal(value, default=0):
    if value in (None, "", "nan", "NaN"):
        return Decimal(str(default))
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return Decimal(str(default))


def _parse_int(value, default=0):
    if value in (None, "", "nan", "NaN"):
        return int(default)
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return int(default)


def _parse_bool(value):
    if value in (None, ""):
        return True
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "active", "enabled"}


def import_medicines(file):
    if not file:
        return 0, 0

    if file.name.endswith(".csv"):
        dataframe = pd.read_csv(file)
    else:
        dataframe = pd.read_excel(file)

    if dataframe.empty:
        return 0, 0

    imported = 0
    updated = 0

    for _, row in dataframe.iterrows():
        raw_data = {str(k): v for k, v in row.items()}
        medicine_name = _get_first_value(raw_data, "medicine_name", "medicine", "product_name", "name")
        if medicine_name in (None, ""):
            continue

        generic_name = _get_first_value(raw_data, "generic_name", "generic") or str(medicine_name)
        category_name = _get_first_value(raw_data, "category", "category_name", "product_category") or "General"
        manufacturer_name = _get_first_value(raw_data, "manufacturer", "manufacturer_name")
        unit = _get_first_value(raw_data, "unit") or "Piece"
        qty = _parse_int(_get_first_value(raw_data, "qty", "quantity", "stock"), 0)
        buying_price = _parse_decimal(_get_first_value(raw_data, "buying_price", "purchase_price", "cost_price"), 0)
        selling_price = _parse_decimal(_get_first_value(raw_data, "selling_price", "sale_price", "price"), 0)
        expiry_date = _get_first_value(raw_data, "expiry_date", "expiry")
        barcode = _get_first_value(raw_data, "barcode", "barcode_no")
        is_active = _parse_bool(_get_first_value(raw_data, "is_active", "status", "active"))

        category = None
        if category_name not in (None, ""):
            category = Category.objects.filter(category_name__iexact=str(category_name)).first()
        if category is None:
            category, _ = Category.objects.get_or_create(
                category_name="General",
                defaults={"description": "Auto-created default category"},
            )

        manufacturer = None
        if manufacturer_name not in (None, ""):
            manufacturer = Manufacturer.objects.filter(manufacturer_name__iexact=str(manufacturer_name)).first()

        medicine_defaults = {
            "medicine_name": str(medicine_name),
            "generic_name": str(generic_name),
            "buying_price": buying_price,
            "selling_price": selling_price,
            "category": category,
            "unit": unit,
            "qty": qty,
            "is_active": is_active,
            "manufacturer": manufacturer,
        }

        if expiry_date not in (None, ""):
            try:
                medicine_defaults["expiry_date"] = pd.to_datetime(expiry_date).date()
            except Exception:
                pass

        if barcode not in (None, ""):
            medicine_defaults["medicine_uuid"] = str(barcode)

        if barcode not in (None, ""):
            existing = Medicine.objects.filter(medicine_uuid=str(barcode)).first()
            if existing:
                for key, value in medicine_defaults.items():
                    setattr(existing, key, value)
                existing.save()
                medicine = existing
                created = False
            else:
                medicine = Medicine(**medicine_defaults)
                medicine.save()
                created = True
        else:
            existing = Medicine.objects.filter(
                medicine_name__iexact=str(medicine_name),
                generic_name__iexact=str(generic_name),
            ).first()
            if existing:
                for key, value in medicine_defaults.items():
                    setattr(existing, key, value)
                existing.save()
                medicine = existing
                created = False
            else:
                medicine = Medicine(**medicine_defaults)
                medicine.save()
                created = True

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
            "Barcode": medicine.medicine_uuid or medicine.id,
            "SKU": medicine.id,
            "Buying Price": medicine.buying_price,
            "Selling Price": medicine.selling_price,
            "Quantity": medicine.qty,
            "Category": medicine.category.category_name if medicine.category else "",
            "Unit": medicine.unit,
            "Expiry Date": medicine.expiry_date,
        }
        for medicine in Medicine.objects.select_related("category").all()
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
