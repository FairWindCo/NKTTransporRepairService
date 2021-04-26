from django.core.management.base import BaseCommand


# delete from trade_products where 1;
# delete from trade_category where 1;
# alter table trade_products AUTO_INCREMENT = 1;
# alter table trade_category AUTO_INCREMENT = 1;
from django.db import IntegrityError

from Product.integration.integration_1c.xls_file_reader import TradeImporter
from Product.models import Categories, Brands, Products


class Command(BaseCommand):
    help = 'Commands for import Category, Product and Brand from 1C export excel file '

    category_cache = {}
    brand_cache = {}
    product_count = 0

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('file_name', type=str, help='<file.xlsx> for import')

        parser.add_argument(
            '--update',
            action='store_true',
            help='Always update products in db',
        )

        parser.add_argument(
            '--update_category',
            action='store_true',
            help='Always update products category in db',
        )

        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='limit processing records',
        )


    def category_create_handler(self, category):
        code = category['code']

        if code in self.category_cache:
            return self.category_cache[code]
        else:
            parent = self.category_cache.get(category['parent']) if category['parent'] else None
            # print('PARENT', parent)
            try:
                category_, added = Categories.objects.get_or_create(code=code, defaults={
                'name': category['name'],
                'code': code,
                'parent': Categories.objects.get(pk=parent['id']) if parent else None,
                })
                category_.save()
                category['id'] = category_.id
                self.category_cache[code] = category
            except IntegrityError as error:
                print('NOT UNIQUE', category, error)
                return None
            return category

    def product_create_handler(self, product, update=False,  update_category=False):
        code = product['code']
        brand_name = str(product['brand']).strip().upper() if product['brand'] else None
        main_category = product['parent']

        if main_category and main_category in self.category_cache:
            parent = self.category_cache.get(main_category)['id']
            main_category = Categories.objects.get(pk=parent)
        else:
            main_category = None

        if brand_name in self.brand_cache:
            brand = self.brand_cache[brand_name]
        else:
            if brand_name:
                try:
                    brand = Brands.objects.get(name__iexact=brand_name)
                    self.brand_cache[brand_name] = brand
                except Brands.DoesNotExist:
                    brand = Brands()
                    brand.name = brand_name
                    brand.save()
                    self.brand_cache[brand_name] = brand
            else:
                brand = None
        need_update = update
        try:
            product_ = Products.objects.get(code=code)
        except Products.DoesNotExist:
            product_ = Products()
            need_update = True

        if need_update:
            product_.name = product['name']
            product_.code = code
            product_.brand = brand
            product_.vendor_code = product['vendor_code']
            try:
                product_.save()
            except IntegrityError as error:
                print('NOT UNIQUE', product, error)
                return None
            except Exception as error:
                print('ERROR', product, error)
                return None
            if main_category:
                product_.categories.add(main_category)
            product_.save()
        if update_category and main_category:
            print(main_category, product_.code)
            product_.categories.add(main_category)
            product_.save()
        product['id'] = product_.id
        self.product_count += 1
        #print(main_category, product, update_category)
        return product

    def handle(self, *args, **options):

        importer = TradeImporter(options['file_name'])
        importer.process_import(lambda cat: self.category_create_handler(cat),
                                lambda pr: self.product_create_handler(pr, options['update'], options['update_category']))

        result = 'PROCESSED UNIQUE CATEGORY {} AND PRODUCTS {} WITH BRANDS {}'.format(
            len(self.category_cache), self.product_count, len(self.brand_cache))
        self.stdout.write(self.style.SUCCESS(result))
        self.stdout.write(self.style.SUCCESS('File imported'))
