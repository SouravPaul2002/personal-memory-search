from backend.services.query_intent_service import (
    detect_query_intent
)

queries = [

    "python code image",

    "red pen photo",

    "database notes",

    "python tutorial pdf",

    "python screenshot",

    "normalization notes"
]

for query in queries:

    print(
        query,
        "->",
        detect_query_intent(query)
    )