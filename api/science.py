import csv
from datetime import date, timedelta

from .models import Document

MIN_YEAR_WEEK = 1
MAX_YEAR_WEEK = 52


def export_publication_history(
    filename,
    start_year=1965,
    end_year=2020,
    header=["Year", "Week", "Publications"],
    delimiter=",",
):
    """Выгрузить данные о еженедельном приросте публикаций
    за заданный исторический период в .csv файл.

    Arguments:
        filename (str): Название файла без расширения.
        start_year (str): Год начала исторического периода.
        end_year (str): Год окончания исторического периода.
        header (Iterable): Заголовок файла.
        delimiter (str): Разделитель между значениями.
        Для корректного экспорта в Excel используйте ";".
    """
    with open(f"{filename}.csv", "w") as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(header)

        publication_count = 0
        for year in range(start_year, end_year + 1):
            for week in range(MIN_YEAR_WEEK, MAX_YEAR_WEEK + 1):
                start_date, end_date = get_date_range(year, week)
                publication_count += get_publication_count_within_range(
                    start_date, end_date
                )
                writer.writerow((year, week, publication_count))


def get_publication_count_within_range(start_date, end_date):
    publications = Document.objects.filter(
        cover_date__range=[start_date, end_date + timedelta(days=1)]
    )
    return publications.count()


def get_date_range(year, week):
    start_date = date.fromisocalendar(year, week, 1)
    end_date = date.fromisocalendar(year, week, 7)
    return start_date, end_date
