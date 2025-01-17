import django_filters
from .models import *

class FoodFilter(django_filters.FilterSet):
    minPrice = django_filters.NumberFilter(field_name="price", lookup_expr='gte', label='Min Price')
    maxPrice = django_filters.NumberFilter(field_name="price", lookup_expr='lte', label='Max Price')

    class Meta:
        model = Food
        fields = ['minPrice', 'maxPrice', 'type', 'cuisine'] #add in discount
