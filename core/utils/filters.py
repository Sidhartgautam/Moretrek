from rest_framework import filters

class TrekCountryCodeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        country_code = request.query_params.get('country_code')
        if country_code:
            queryset = queryset.filter(country__code__iexact=country_code)
        return queryset