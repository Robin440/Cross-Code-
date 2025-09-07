from rest_framework.response import Response
from rest_framework import status


def response_processor(message, status_code, data=None):
    response = {
        'message': message,
        'data': data
    }
    return Response(response, status=status_code)


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

