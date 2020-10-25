from django.http import JsonResponse

from .science import get_publication_history


def publication_history(request):
    start_year = request.GET.get("start_year", 1965)
    end_year = request.GET.get("end_year", 2020)

    history = get_publication_history(start_year, end_year)
    payload = []
    for record in history:
        payload.append(
            {
                "year": record.year,
                "week": record.week,
                "publications": record.publications,
            }
        )

    return JsonResponse(payload, safe=False)
