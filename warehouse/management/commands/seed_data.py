import random
from django.core.management.base import BaseCommand
from warehouse.models import Warehouse, Product, Supplier

class Command(BaseCommand):
    help = "Seed database with fake data for Warehouse, Product, Supplier"

    def handle(self, *args, **kwargs):
        # Oldingi malumotlarni o'chirish
        Warehouse.objects.all().delete()
        Product.objects.all().delete()
        Supplier.objects.all().delete()

        # Warehouse yaratish
        warehouses = []
        for i in range(1, 21):
            w = Warehouse.objects.create(
                name=f"Warehouse {i}",
                location=f"Location {i}",
                capacity=random.randint(500, 5000),
            )
            warehouses.append(w)

        # Supplier yaratish
        suppliers = []
        for i in range(1, 21):
            s = Supplier.objects.create(
                name=f"Supplier {i}",
                contact_info=f"+99890{random.randint(1000000,9999999)}",
            )
            suppliers.append(s)

        # Product yaratish
        for i in range(1, 21):
            Product.objects.create(
                name=f"Product {i}",
                description=f"This is description for product {i}.",
                price=round(random.uniform(10.0, 500.0), 2),
                quantity=random.randint(1, 200),
                warehouse=random.choice(warehouses),
                supplier=random.choice(suppliers),
            )

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully with fake data!"))
