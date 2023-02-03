import traceback

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging


# def custom_exception_handler(exc, context):
#     logger = logging.getLogger(__name__)
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)

#     if response is not None:
#         logger.warning(response.data)

#     else:
#         response = Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
#         logger.error('Unhandled Exception')
#         logger.error(str(exc))
#         logger.error(traceback.format_exc())

#     return response