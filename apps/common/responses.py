from rest_framework.response import Response

def success_response(data=None, message=""):
    return Response({
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    })

def error_response(message="An error occurred", errors=None, status_code=400):
    return Response({
        "success": False,
        "message": message,
        "errors": errors if errors is not None else {}
    }, status=status_code)
