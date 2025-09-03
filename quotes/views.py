import json
import random
import uuid
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from django.db.models import F

from quotes.models import Quote, QuoteReaction, Statistics


def index(request: HttpRequest):
    stats, _ = Statistics.objects.get_or_create(id=1)
    Statistics.objects.filter(id=stats.id).update(total_views=F("total_views") + 1)
    stats.refresh_from_db()

    quotes = list(Quote.objects.all())

    if len(quotes) == 0:
        return render(
            request,
            "quotes/index.html",
            {"quote": None},
        )

    quote = random.choices(quotes, weights=[q.weight for q in quotes], k=1)[0]

    user_uuid = get_or_create_user_uuid(request)

    score = quote.reactions.filter(user_uuid=user_uuid).first()

    print(score)
    response = render(
        request,
        "quotes/index.html",
        {"total_views": stats.total_views, "quote": quote, "score": score},
    )

    response.set_cookie("user_uuid", user_uuid)

    return response


@require_http_methods(["POST"])
def add_or_update_quote_reaction(request: HttpRequest, quote_id: int):
    data = json.loads(request.body.decode("utf-8"))

    reaction_type = data.get("type")

    quote = get_object_or_404(Quote, id=quote_id)

    if reaction_type not in [QuoteReaction.LIKE, QuoteReaction.DISLIKE]:
        return JsonResponse(
            {"success": False, "error": "Invalid reaction type"}, status=400
        )

    user_uuid = get_or_create_user_uuid(request)

    QuoteReaction.objects.update_or_create(
        quote=quote, user_uuid=user_uuid, defaults={"type": reaction_type}
    )

    response = JsonResponse({"success": True})
    response.set_cookie("user_uuid", user_uuid)

    return response


def get_or_create_user_uuid(request: HttpRequest):
    user_uuid = request.COOKIES.get("user_uuid")

    if not user_uuid:
        user_uuid = str(uuid.uuid4())

    return user_uuid
