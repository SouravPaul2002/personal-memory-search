from backend.services.hybrid_search_service import (
    hybrid_search
)

results = hybrid_search(
    "red pen"
)

print("\nTEXT RESULTS\n")
print(results["text_results"])

print("\nCLIP RESULTS\n")
print(results["clip_results"])