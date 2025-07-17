from app.repositories import _candidate_repository

def call(request):
    mobile_number = request.get('mobile_number')
    if (candidate:=~_candidate_repository().find_one({'mobile_number': mobile_number})):
        return _candidate_repository().update(candidate, request)
    
    email = request.get('email')
    if (candidate:=~_candidate_repository().find_one({'email': email})):
        return _candidate_repository().update(candidate, request)
    
    candidate = _candidate_repository().create(**request)

    return candidate