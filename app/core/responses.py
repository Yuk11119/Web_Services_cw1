def success_response(data, meta=None):
    return {"data": data, "meta": meta or {}}


def error_response(error_code: str, message: str, details=None):
    return {"error_code": error_code, "message": message, "details": details or {}}
