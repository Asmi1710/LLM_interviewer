from app.lib.helpers.search_helper import parse_conditions
from app.repositories import _candidate_repository


def call(conditions, offset=None, limit=None, sort_column=None, sort_order=None):
    _sort = f"-{sort_column}" if sort_column and sort_order == 'desc' else sort_column

    search_conditions = parse_conditions(conditions)
    candidate_query = _candidate_repository().find(search_conditions)
    candidates = ~candidate_query.skip(offset).limit(limit).sort(_sort)

    return {
        "candidates": candidates,
        "offset": offset,
        "limit": limit,
        "sort_column": sort_column,
        "sort_order": sort_order,
        "count": len(candidates),
        "total": candidate_query.count()
    }

