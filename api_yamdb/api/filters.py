from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class TitlesFilter(FilterSet):
    genre = CharFilter(method='filter_by_genre')
    category = CharFilter(method='filter_by_category')
    name = CharFilter(method='filter_by_name')

    class Meta:
        model = Title
        fields = ('year',)

    def filter_by_genre(self, queryset, name, value):
        return queryset.filter(genre__slug=value)

    def filter_by_category(self, queryset, name, value):
        return queryset.filter(category__slug=value)

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(name=value)
