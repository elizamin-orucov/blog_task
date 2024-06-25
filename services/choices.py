from datetime import datetime

now_date = int(datetime.now().strftime("%Y")) + 1


def year_choice():
    return ((year, year) for year in range(2011, now_date))


BLOG_STATUS = (
    ("Active", "Active"),
    ("Deactivate", "Deactivate"),
)
