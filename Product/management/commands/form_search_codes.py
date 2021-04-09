from django.core.management import BaseCommand

from Trade.models import Products, simplify_vendor_code


class Command(BaseCommand):
    help = 'Form search codes for products'

    def handle(self, *args, **options):
        products = Products.objects.filter(vendor_code__isnull=False)

        products = products.filter(search_code__isnull=True) | products.filter(search_code__exact='')

        index = 0
        for product in products:
            result = simplify_vendor_code(product.vendor_code)
            if not result:
                print(product, product.vendor_code, result)
                break
            product.search_code = result
            product.save()
            index += 1
            if index % 1000 == 0:
                print("PROCESSED {} records".format(index))

