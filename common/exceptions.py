from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None
    detail = response.data.get("detail", response.data) if isinstance(response.data, dict) else response.data
    response.data = {"code": response.status_code, "message": detail, "data": None}
    return response


def api_response(data=None, message="ok", code=200):
    return Response({"code": code, "message": message, "data": data}, status=code)

