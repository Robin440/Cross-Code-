from threading import local
_thread_locals = local()
class RequestContextMiddleware:
    """
    Middleware to store the current request in thread-local storage.
    This allows access to the request object from anywhere in the code.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        request.username = getattr(request.user, 'username', 'anonymous') if hasattr(request, 'user') else 'anonymous'
        response = self.get_response(request)
        return response