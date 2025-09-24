from rest_framework.response import Response
from rest_framework import status


def response_processor(message: str, status_code: int, data=None, success: bool = False) -> Response:
    """
    Standardized API response.

    :param message: Message string for response
    :param status_code: HTTP status code
    :param data: Optional payload
    :param success: True if operation succeeded, False otherwise
    :return: DRF Response object
    """
    response = {
        'message': message,
        'data': data,
        'status': "success" if success else "failed"
    }
    return Response(response, status=status_code)

def error_response(request, message, errors=None, status_code=400, template_name=None):
    """
    Standardize error responses for HTML and JSON formats.
    
    Args:
        request: The Django request object to determine renderer format.
        message (str): The error message to include in the response.
        errors (dict, optional): Additional error details (e.g., serializer errors).
        status_code (int): HTTP status code (default: 400).
        template_name (str, optional): Template name for HTML responses.
    
    Returns:
        Response: A REST framework Response object for HTML or JSON.
    """
    error_data = {"error": message}
    if errors:
        error_data["errors"] = errors
    if request.accepted_renderer.format == "html" and template_name:
        return Response(error_data, template_name=template_name, status=status_code)
    return Response(error_data, status=status_code)
class ResponseService:
    @staticmethod
    def HTTP_200(data,template_name=None) -> Response:
        if isinstance(data, dict) is False:
            data = {"message": data}
        return Response(data, status=status.HTTP_400_BAD_REQUEST, template_name=template_name)

    @staticmethod
    def HTTP_201(data,template_name=None) -> Response:
        if isinstance(data, dict) is False:
            data = {"message": data}
        return Response(data, status=status.HTTP_400_BAD_REQUEST, template_name=template_name)

    @staticmethod
    def HTTP_202(data,template_name=None) -> Response:
        if isinstance(data, dict) is False:
            data = {"message": data}
        return Response(data, status=status.HTTP_400_BAD_REQUEST, template_name=template_name)

    @staticmethod
    def HTTP_204(data,template_name=None) -> Response:
        if isinstance(data, dict) is False:
            data = {"message": data}
        return Response(data, status=status.HTTP_400_BAD_REQUEST, template_name=template_name)

    @staticmethod
    def HTTP_400(data,template_name=None) -> Response:
        if isinstance(data, dict) is False:
            data = {"error": data}
        return Response(data, status=status.HTTP_400_BAD_REQUEST, template_name=template_name)

    @staticmethod
    def HTTP_401(data,template_name=None) -> Response:
        if isinstance(data, dict) is False:
            data = {"error": data}
        return Response(data, status=status.HTTP_400_BAD_REQUEST, template_name=template_name)

    @staticmethod
    def HTTP_403(data,template_name=None) -> Response:
        if isinstance(data, dict) is False:
            data = {"error": data}
        return Response(data, status=status.HTTP_400_BAD_REQUEST, template_name=template_name)

    @staticmethod
    def HTTP_404(data,template_name=None) -> Response:
        if isinstance(data, dict) is False:
            data = {"error": data}
        return Response(data, status=status.HTTP_400_BAD_REQUEST, template_name=template_name)

    @staticmethod
    def HTTP_307(data,template_name=None) -> Response:
        if isinstance(data, dict) is False:
            data = {'error':data}
        return Response(data, status=status.HTTP_400_BAD_REQUEST, template_name=template_name)

    @staticmethod
    def HTTP_408(data,template_name=None) -> Response:
        if isinstance(data, dict) is False:
            data = {'error':data}
        return Response(data, status=status.HTTP_400_BAD_REQUEST, template_name=template_name)

