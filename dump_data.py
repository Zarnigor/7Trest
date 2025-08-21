from warehouse.models import Category, Unit, Product, StockMovement
from decimal import Decimal
from datetime import datetime

def run():
    # === Units ===
    unit_names = [
        ("штук", "шт"),
        ("килограмм", "кг"),
        ("литр", "л"),
        ("метр", "м"),
        ("рулон", "рул"),
    ]

    units = {}
    for name, abbr in unit_names:
        u, _ = Unit.objects.get_or_create(name=name, abbreviation=abbr)
        units[abbr] = u

    # === Categories ===
    category_names = [
        "Строительные материалы",
        "Отделочные материалы",
        "Электрика",
        "Сантехника",
        "Инструменты",
    ]

    categories = {}
    for name in category_names:
        c, _ = Category.objects.get_or_create(name=name)
        categories[name] = c

    # === Products + StockMovements ===
    products_data = [
        ("Строительные материалы", "4600000000001", "Арматура 12мм", "шт", 103, 257.5, 72, 194.67, 5, 12.88),
        ("Строительные материалы", "4600000000002", "Цемент М500", "шт", 106, 265, 74, 200.34, 5, 13.35),
        # ... qolganlarini shu ketma-ketlikda qo'shish mumkin ...
    ]

    for row in products_data:
        cat_name, barcode, name, unit_abbr, in_qty, in_val, out_qty, out_val, ret_qty, ret_val = row

        product, _ = Product.objects.get_or_create(
            name=name,
            barcode=barcode,
            category=categories[cat_name],
            unit=units[unit_abbr]
        )

        StockMovement.objects.create(
            product=product,
            movement_type="inbound",
            quantity=Decimal(in_qty),
            total_value=Decimal(in_val),
            created_at=datetime(2025, 8, 10)
        )
        StockMovement.objects.create(
            product=product,
            movement_type="outbound",
            quantity=Decimal(out_qty),
            total_value=Decimal(out_val),
            created_at=datetime(2025, 8, 11)
        )
        StockMovement.objects.create(
            product=product,
            movement_type="return",
            quantity=Decimal(ret_qty),
            total_value=Decimal(ret_val),
            created_at=datetime(2025, 8, 12)
        )
