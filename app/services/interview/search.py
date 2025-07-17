from app.lib.helpers.search_helper import parse_conditions
from app.repositories import _interview_repository


def call(conditions, offset=None, limit=None, sort_column=None, sort_order=None):
    _sort = f"-{sort_column}" if sort_column and sort_order == 'desc' else sort_column

    search_conditions = parse_conditions(conditions)
    interview_query = _interview_repository().find(search_conditions)
    interviews = ~interview_query.skip(offset).limit(limit).sort(_sort)

    return {
        "interviews": interviews,
        "offset": offset,
        "limit": limit,
        "sort_column": sort_column,
        "sort_order": sort_order,
        "count": len(interviews),
        "total": interviews.count()
    }