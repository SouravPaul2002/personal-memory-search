import yake
from collections import Counter


def extract_keywords(
    text,
    max_keywords=10
):
    keyword_extractor = yake.KeywordExtractor(
        lan="en",
        n=2,
        dedupLim=0.9,
        top=max_keywords
    )

    keywords = keyword_extractor.extract_keywords(
        text
    )

    cleaned_keywords = []

    for keyword, score in keywords:

        keyword = keyword.strip()

        if len(keyword) < 3:
            continue

        if keyword.lower() not in [
            k.lower()
            for k in cleaned_keywords
        ]:
            cleaned_keywords.append(
                keyword
            )

    return cleaned_keywords


def extract_chunk_keywords(
    chunks,
    max_keywords=10
):

    keyword_extractor = yake.KeywordExtractor(
        lan="en",
        n=2,
        dedupLim=0.9,
        top=max_keywords
    )

    all_keywords = []

    for chunk in chunks:

        keywords = keyword_extractor.extract_keywords(
            chunk
        )

        for keyword, score in keywords:

            keyword = keyword.strip()

            if len(keyword) < 3:
                continue

            all_keywords.append(
                keyword
            )

    return all_keywords


def build_topics(
    keywords,
    top_n=30
):

    counter = Counter()

    for keyword in keywords:

        counter[
            keyword.lower()
        ] += 1

    return [
        keyword
        for keyword, count in counter.most_common(
            top_n
        )
    ]


def build_enriched_text(
    chunk_text,
    keywords
):

    keywords_text = " ".join(
        keywords
    )

    return (
        f"{keywords_text}\n\n"
        f"{chunk_text}"
    )