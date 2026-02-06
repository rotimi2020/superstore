import csv
import os
from decimal import Decimal, InvalidOperation
from datetime import datetime

from django.core.management.base import BaseCommand
from superstore_app.models import SuperstoreDashboard


class Command(BaseCommand):
    help = 'Import Superstore CSV data (clean dates, safe reload)'

    BATCH_SIZE = 1000

    # -------------------------
    # HELPERS
    # -------------------------
    def parse_decimal(self, value, default='0'):
        try:
            return Decimal(str(value).strip())
        except (InvalidOperation, TypeError, ValueError):
            return Decimal(default)

    def parse_int(self, value, default=0):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return default

    def parse_date(self, value):
        """
        Accepts:
        - MM/DD/YYYY
        - YYYY-MM-DD
        Returns datetime.date or None
        """
        if not value:
            return None

        value = str(value).strip()
        for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                pass
        return None

    # -------------------------
    # MAIN
    # -------------------------
    def handle(self, *args, **options):
        csv_file = 'superstore.csv'

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file}'))
            return

        # 🔥 Step 1: Clear old data
        deleted, _ = SuperstoreDashboard.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Deleted {deleted} old records'))

        batch = []
        imported = 0
        skipped = 0

        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row_num, row in enumerate(reader, start=1):
                order_date = self.parse_date(row.get('Order Date'))
                ship_date = self.parse_date(row.get('Ship Date'))

                if not order_date:
                    skipped += 1
                    self.stdout.write(
                        self.style.WARNING(f'Row {row_num} skipped: invalid Order Date')
                    )
                    continue

                try:
                    batch.append(
                        SuperstoreDashboard(
                            order_date=order_date,
                            ship_date=ship_date,
                            ship_mode=row.get('Ship Mode', 'Standard Class'),
                            segment=row.get('Segment', 'Consumer'),
                            region=row.get('Region', 'Central'),
                            state=row.get('State', ''),
                            city=row.get('City', ''),
                            category=row.get('Category', 'Office Supplies'),
                            sub_category=row.get('Sub-Category', ''),
                            sales=self.parse_decimal(row.get('Sales')),
                            profit=self.parse_decimal(row.get('Profit')),
                            quantity=self.parse_int(row.get('Quantity')),
                            discount=self.parse_decimal(row.get('Discount')),
                        )
                    )
                    imported += 1

                    if len(batch) >= self.BATCH_SIZE:
                        SuperstoreDashboard.objects.bulk_create(batch)
                        batch.clear()

                except Exception as e:
                    skipped += 1
                    self.stdout.write(
                        self.style.ERROR(f'Row {row_num} failed: {e}')
                    )

            if batch:
                SuperstoreDashboard.objects.bulk_create(batch)

        self.stdout.write(self.style.SUCCESS('IMPORT COMPLETE'))
        self.stdout.write(self.style.SUCCESS(f'Imported: {imported}'))
        self.stdout.write(self.style.WARNING(f'Skipped: {skipped}'))
