def keyword_match_score(
    query,
    keywords
):
    query_words = set(
        query.lower().split()
    )

    score = 0

    for keyword in keywords:

        keyword_words = set(
            keyword.lower().split()
        )

        score += len(
            query_words.intersection(
                keyword_words
            )
        )

    return score