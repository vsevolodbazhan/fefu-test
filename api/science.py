from collections import namedtuple
from datetime import date, timedelta

from .models import Document

MIN_YEAR_WEEK = 1
MAX_YEAR_WEEK = 52

PublicationRecord = namedtuple("PublicationRecord", ["year", "week", "publications"])
PublicationRecord.__doc__ = (
    "Запись о количестве публикаций в определенную неделю определенного года."
)


def get_publication_history(
    start_year=1965,
    end_year=2020,
):
    """Получить данные о еженедельном приросте публикаций
    за заданный исторический период.

    Arguments:
        start_year (str): Год начала исторического периода.
        end_year (str): Год окончания исторического периода.

    Returns:
        list[PublicationRecord]: Список исторических записей.
    """
    records = []
    publication_count = 0
    for year in range(start_year, end_year + 1):
        for week in range(MIN_YEAR_WEEK, MAX_YEAR_WEEK + 1):
            start_date, end_date = get_date_range(year, week)
            publication_count += get_publication_count_within_range(
                start_date, end_date
            )
            record = PublicationRecord(year, week, publication_count)
            records.append(record)
    return records


def get_publication_count_within_range(start_date, end_date):
    publications = Document.objects.filter(
        cover_date__range=[start_date, end_date + timedelta(days=1)]
    )
    return publications.count()


def get_date_range(year, week):
    start_date = date.fromisocalendar(year, week, 1)
    end_date = date.fromisocalendar(year, week, 7)
    return start_date, end_date
