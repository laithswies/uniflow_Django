from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
import logging
from rest_framework.exceptions import APIException
from rest_framework import status
logger = logging.getLogger('Exception')


class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(
            exception
        )
        if isinstance(exception, IntegrityError):
            return JsonResponse({'error': 'AlreadyExists'}, status=409)
        if isinstance(exception, ValidationError):
            return JsonResponse({'error': 'Bad Request'}, status=400)
        if isinstance(exception, Unauthorized):
            return JsonResponse({'detail': exception.default_detail}, status=exception.status_code)
        return None


class Unauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized'
    default_code = 'unauthorized'

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail
        else:
            self.detail = self.default_detail

        super().__init__(detail=self.detail)
