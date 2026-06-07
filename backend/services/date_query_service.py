from datetime import datetime, timedelta


def extract_time_filter(
    query
):

    query = query.lower()

    today = datetime.now()

    if "today" in query:

        start = today.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        return start.timestamp()

    if "yesterday" in query:

        start = (
            today - timedelta(days=1)
        ).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        return start.timestamp()

    if "last week" in query:

        start = today - timedelta(days=7)

        return start.timestamp()

    if "last month" in query:

        start = today - timedelta(days=30)

        return start.timestamp()

    return None