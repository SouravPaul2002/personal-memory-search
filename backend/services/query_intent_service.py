IMAGE_WORDS = {
    "image",
    "photo",
    "picture",
    "pic",
    "screenshot",
    "wallpaper"
}

TEXT_WORDS = {
    "pdf",
    "notes",
    "document",
    "ebook",
    "tutorial",
    "guide",
    "study",
    "material"
}


def detect_query_intent(query):

    query = query.lower()

    image_score = 0
    text_score = 0

    for word in IMAGE_WORDS:

        if word in query:
            image_score += 1

    for word in TEXT_WORDS:

        if word in query:
            text_score += 1

    # screenshot + code = hybrid
    if (
        "screenshot" in query
        and (
            "python" in query
            or "code" in query
            or "program" in query
            or "script" in query
        )
    ):
        return "hybrid"

    if image_score > 0 and text_score > 0:
        return "hybrid"

    if image_score > 0:
        return "image"

    if text_score > 0:
        return "text"

    return "text"