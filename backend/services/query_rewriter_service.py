def rewrite_query(query):

    query = query.lower()

    result = {
        "search_type": "all",
        "keywords": []
    }

    # Detect file type

    if any(word in query for word in [
        "pdf",
        "document",
        "documents"
    ]):
        result["search_type"] = "pdf"

    elif any(word in query for word in [
        "image",
        "photo",
        "picture"
    ]):
        result["search_type"] = "image"

    elif "screenshot" in query:
        result["search_type"] = "image"

    # Remove useless words

    stopwords = {
        "the",
        "i",
        "my",
        "before",
        "after",
        "related",
        "about",
        "containing",
        "contains",
        "with",
        "a",
        "an",
        "of",
        "for",
        "to",
        "in",
        "on",

        # file type words
        "pdf",
        "document",
        "documents",
        "file",
        "files",
        "image",
        "photo",
        "picture",
        "screenshot",

        # memory-query noise
        "studied",
        "study",
        "exam",
        "material",
        "guide",
        "tutorial",
        "learning",
        "learn",
        "containing",
        "contains",
        "saved",
        "downloaded",
        "opened",
        "used",
        "looking",
        "find",
        "search"
    }

    keywords = []

    for word in query.split():

        word = word.strip()

        if len(word) < 2:
            continue

        if word in stopwords:
            continue

        keywords.append(word)

    result["keywords"] = keywords

    return result