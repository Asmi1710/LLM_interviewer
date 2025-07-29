from app.lib.helpers.search_helper import parse_conditions
from app.repositories import _job_repository


def call(conditions, offset=None, limit=None, sort_column=None, sort_order=None):
    _sort = f"-{sort_column}" if sort_column and sort_order == 'desc' else sort_column

    search_conditions = parse_conditions(conditions)
    job_query = _job_repository().find(search_conditions)
    jobs = ~job_query.skip(offset).limit(limit).sort(_sort)

    return {
        "jobs": jobs,
        "offset": offset,
        "limit": limit,
        "sort_column": sort_column,
        "sort_order": sort_order,
        "count": len(jobs),
        "total": job_query.count()
    }