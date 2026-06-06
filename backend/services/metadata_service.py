import yake


def extract_keywords(
    text,
    max_keywords=10
):
    keyword_extractor = yake.KeywordExtractor(
        lan="en",
        n=2,
        dedupLim=0.8,
        top=max_keywords
    )

    keywords = keyword_extractor.extract_keywords(text)

    cleaned_keywords = []

    for keyword, score in keywords:

        keyword = keyword.strip()

        if len(keyword) < 3:
            continue

        if keyword.lower() not in [
            k.lower()
            for k in cleaned_keywords
        ]:
            cleaned_keywords.append(keyword)

    return cleaned_keywords