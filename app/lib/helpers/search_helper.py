# https://www.mongodb.com/docs/manual/reference/operator/query/
from bunnet.odm.fields import PydanticObjectId
from app.lib.helpers import parse_datetime

SEARCH_OPTIONS = ['limit', 'offset', 'sort_column', 'sort_order']


def get_search_options(request):
    options = {key: request.get(key) for key in SEARCH_OPTIONS if key in request}
    options = {
                  'limit': 100,
                  'offset': None,
                  'sort_column': 'updated_at',
                  'sort_order': 'desc'
              } | options
    if request.get('skip_limit') == True:
        options['limit'] = None
    elif not options['offset']:
        options['offset'] = get_offset(request.get('page', 1), options['limit'])

    return options


def get_offset(page=1, limit=10):
    return ((page or 1) - 1) * limit


def parse_conditions(conditions):
    parsed_conditions = {}
    for key, value in conditions.items():
        match key:
            case 'and':
                if type(value) == list:
                    parsed_conditions["$and"] = [parse_conditions(sub_conditions) for sub_conditions in value]
                elif type(value) == dict:
                    parsed_conditions["$and"] = [{attr_name: parse_value(attr_cond)} for attr_name, attr_cond in
                                                 value.items()]
            case 'or':
                if type(value) == list:
                    parsed_conditions["$or"] = [parse_conditions(sub_conditions) for sub_conditions in value]
                elif type(value) == dict:
                    parsed_conditions["$or"] = [{attr_name: parse_value(attr_cond)} for attr_name, attr_cond in
                                                value.items()]
            case _:
                parsed_conditions[key] = parse_value(value)
    return parsed_conditions


def parse_value(hash):
    if not (type(hash) == dict and 'operator' in hash): return {"$eq": hash}

    operator = hash['operator']
    value_type = hash.get('type')
    value = typecast(hash.get('value'), value_type)

    match operator:
        case op if op in ['eq', 'gt', 'gte', 'in', 'lt', 'lte', 'ne', 'nin', 'all', 'size', 'exists', 'type', 'mod']:
            return {f"${op}": value}
        case 'neq':
            return {"$ne": value}
        case 'not':
            return {"$not": value}  # handle repeated conditions
        case 'regex':
            options = hash.get('options')
            val = {"$regex": value, '$options' : 'i'}
            if options: val['$optiions'] = options
            return val
        case 'contains':
            return {"$regex": f".*{value}.*", '$options' : 'i'}
        case 'not_contains':
            return {"$not": {"$regex": f".*{value}.*", '$options' : 'i'}}
        case 'starts_with':
            return {"$regex": f"{value}.*", '$options' : 'i'}
        case 'ends_with':
            return {"$regex": f".*{value}", '$options' : 'i'}
        case 'is_empty':
            return {"$eq": None}
        case 'not_empty':
            return {"$ne": None}
        case 'between':
            if type(value)==list: return {"$gte": value[0], "$lte": value[1]}
        case 'near':
            max_distance = hash.get('max_distance')
            val = {"$near": value}
            if max_distance: val['$maxDistance'] = max_distance
            return val
        case _:
            return {"$eq": value}


def typecast(value, value_type):
    if type(value) == list:
        return [typecast(val, value_type) for val in value]

    match value_type:
        case 'id':
            return PydanticObjectId(value)
        case typ if typ in ['date', 'datetime']:
            return parse_datetime(value)
        case _:
            return value
