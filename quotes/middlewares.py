from quotes.util import get_or_create_user_uuid


class UuidMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response.set_cookie("user_uuid", get_or_create_user_uuid(request))

        return response