from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    print(exc, context)
    error = "%s %s %s" % (context['view'], context['request'].method, exc)
    print(error)
    if response is None:
        print("111111")
        return Response(
            {"error": "请稍等一会"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)
    return response