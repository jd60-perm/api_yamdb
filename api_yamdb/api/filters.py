import django_filters
from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.Filter(
        field_name='category__slug', lookup_expr='exact'
    )
    genre = django_filters.Filter(
        field_name='genre__slug', lookup_expr='exact'
    )
    name = django_filters.Filter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')
