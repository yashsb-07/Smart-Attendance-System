from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Global exception handler for the entire project.
    """

    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {
                "success": False,
                "message": "An unexpected error occurred.",
                "errors": None,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    message = "Request failed."

    if isinstance(response.data, dict):
        if "detail" in response.data:
            message = response.data["detail"]
            errors = None
        else:
            errors = response.data
    else:
        errors = response.data

    return Response(
        {
            "success": False,
            "message": message,
            "errors": errors,
        },
        status=response.status_code,
    )