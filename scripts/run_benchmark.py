import json

from backend.services.fusion_search_service import (
    fusion_search
)

with open(
    "docs/search_benchmark.json",
    "r",
    encoding="utf-8"
) as f:

    benchmark = json.load(f)

total = len(benchmark)
correct = 0

for test in benchmark:

    query = test["query"]
    expected = test["expected"]

    results = fusion_search(query)

    found = False

    for result in results[:5]:

        file_name = result.get(
            "file_name",
            ""
        )

        if file_name.lower() == expected.lower():

            found = True
            correct += 1
            break

    print(
        f"{query} -> "
        f"{'PASS' if found else 'FAIL'}"
    )

    if not found:

        print("\nFAIL")
        print("Query:", query)
        print("Expected:", expected)
        print("Top Results:")

        for result in results[:5]:

            print(
                result.get(
                    "file_name",
                    "Unknown"
                )
            )

        print()

print("\n----------------")

print(
    f"Accuracy: "
    f"{correct}/{total}"
)

print(
    f"{(correct / total) * 100:.2f}%"
)