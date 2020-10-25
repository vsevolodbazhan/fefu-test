from http import HTTPStatus

from django.http import JsonResponse, HttpResponse

from .science import get_publication_history


def publication_history(request):
    """
    paths:
      /api/documents/history:
        get:
          operationId: getPublicationHistory
          description: Получить историю публикаций.
          parameters:
            - in: query
              name: startYear
              schema:
                type: integer
                default: 1965
              description: Начало исторического периода.
            - in: query
              name: endYear
              schema:
                type: integer
                defaul: 2020
              description: Конец исторического периода.
          responses:
              200:
                description: История публикаций.
                content:
                  application/json:
                    schema:
                      type: array
                      items:
                        type: object
                        properties:
                          year:
                            type: integer
                            description: Год
                          week:
                            type: interger
                            description: Неделя
                          publications:
                            type: intger
                            description: Количество публикаций
              204:
                description: Публикации отсутствуют.
              400:
                description: Некорректный запрос.
                content:
                  application/json:
                    schema:
                      type: object
                      properties:
                        message:
                          description: Сообщение об ошибке.
                          type: string
    """

    if request.method != "GET":
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)

    start_year = request.GET.get("startYear", 1965)
    end_year = request.GET.get("endYear", 2020)

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
