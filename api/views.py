from http import HTTPStatus

from django.http import JsonResponse, HttpResponse

from .science import get_publication_history


def publication_history(request):
    if request.method != "GET":
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)

    start_year = request.GET.get("start_year", 1965)
    end_year = request.GET.get("end_year", 2020)

    try:
        start_year = int(start_year)
        end_year = int(end_year)
    except ValueError:
        payload = {"error": "`start_year` and `end_year` must be integer numbers."}
        return JsonResponse(payload, status=HTTPStatus.BAD_REQUEST)

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

    if not payload:
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    return JsonResponse(payload, safe=False)
