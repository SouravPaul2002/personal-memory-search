from backend.services.query_rewriter_service import (
    rewrite_query
)

queries = [

    "the pdf i studied before my dbms exam",

    "the screenshot about normalization",

    "red pen image",

    "python notes pdf",

    "machine learning document"

]

for query in queries:

    print("\nQUERY:")
    print(query)

    print(
        rewrite_query(query)
    )