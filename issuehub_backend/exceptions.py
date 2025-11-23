from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns errors in the format:
    {error: {code, message, details?}}
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': {
                'code': response.status_code,
                'message': str(exc),
            }
        }
        
        # Add details if available
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                custom_response_data['error']['details'] = exc.detail
            elif isinstance(exc.detail, list):
                custom_response_data['error']['details'] = exc.detail

        response.data = custom_response_data

    return response

