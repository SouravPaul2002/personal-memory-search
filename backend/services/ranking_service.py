def filename_match_score(
    query,
    filename
):

    query_words = (
        query.lower().split()
    )

    filename = (
        filename.lower()
    )

    score = 0

    for word in query_words:

        if word in filename:
            score += 3

    return score