"""Metadata pre-filtering: build a Chroma `where` clause from a business
profile so retrieval never surfaces rules outside the business's actual
state/industry/category.
"""


def build_where_filter(state: str | None = None, industry: str | None = None,
                        category: str | None = None) -> dict | None:
    clauses = []

    if state:
        clauses.append({"applicable_state": {"$in": [state, "central"]}})
    if industry:
        clauses.append({"applicable_industry": {"$in": [industry, "all"]}})
    if category:
        clauses.append({"regulation_category": category})

    if not clauses:
        return None
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}
