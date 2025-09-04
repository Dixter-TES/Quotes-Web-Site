import uuid

from django.http import HttpRequest


def get_or_create_user_uuid(request: HttpRequest):
    user_uuid = request.COOKIES.get("user_uuid")

    if not user_uuid:
        user_uuid = str(uuid.uuid4())

    return user_uuid
