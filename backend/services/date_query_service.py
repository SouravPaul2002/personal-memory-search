from datetime import datetime, timedelta


def extract_time_filter(
    query
):

    query = query.lower()

    today = datetime.now()

    today_start = today.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    if "today" in query:

        return today_start.timestamp(), today.timestamp()

    if "yesterday" in query:

        yesterday_start = today_start - timedelta(days=1)

        return yesterday_start.timestamp(), today_start.timestamp()

    if "last week" in query:

        start = today_start - timedelta(days=7)

        return start.timestamp(), today.timestamp()

    if "last month" in query:

        start = today_start - timedelta(days=30)

        return start.timestamp(), today.timestamp()

    return None