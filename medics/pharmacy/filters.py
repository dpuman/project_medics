import django_filters
from django_filters import CharFilter


from .models import *


class PharmacyFilter(django_filters.FilterSet):
    area = CharFilter(field_name='area', lookup_expr='icontains')

    class Meta:
        model = Pharmacy
        fields = ['area', ]


class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', ]


class PharmacyProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', ]
