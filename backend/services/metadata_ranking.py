def metadata_score(
    query,
    topics,
    summary
):

    query = query.lower()

    score = 0

    for topic in topics:

        if topic.lower() in query:
            score += 5

    if summary:

        summary = summary.lower()

        for word in query.split():

            if word in summary:
                score += 1

    return score