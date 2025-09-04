import json
import random
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import F
from django.db.models import Avg, Count, Q
from django.views.decorators.csrf import csrf_exempt

from quotes.forms import QuoteForm
from quotes.models import Quote, QuoteReaction, Statistics
from quotes.util import get_or_create_user_uuid


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
    user_reaction = quote.reactions.filter(user_uuid=user_uuid).first()

    response = render(
        request,
        "quotes/index.html",
        {
            "total_views": stats.total_views,
            "quote": quote,
            "reaction": user_reaction.type if user_reaction else None,
        },
    )

    return response


def rating(request: HttpRequest):
    top_10_quotes = Quote.objects.annotate(
        likes_count=Count("reactions", filter=Q(reactions__type=QuoteReaction.LIKE))
    ).order_by("-likes_count")[:10]

    return render(request, "quotes/rating.html", {"quotes": top_10_quotes})


def editor(request: HttpRequest, quote_id: int = None):
    if quote_id:
        quote = get_object_or_404(Quote, id=quote_id)
    else:
        quote = None
        
    show_form = False
    form_title = "Изменение цитаты"

    if request.method == "POST":
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            saved_quote = form.save()
            if not saved_quote:
                print("Quote not saved!")
            return redirect("editor")
        else:
            show_form = True
    else:
        form = QuoteForm(instance=quote)
        
        if quote_id:
            show_form = True

    quotes = list(Quote.objects.all())
    
    return render(request, "quotes/editor.html", {"quotes": quotes, "form": form, "show_form": show_form, "form_title": form_title})


@csrf_exempt
@require_http_methods(["POST"])
def add_or_update_quote_reaction(request: HttpRequest, quote_id: int):
    reaction_type = request.POST.get("type")

    quote = get_object_or_404(Quote, id=quote_id)

    if reaction_type not in [QuoteReaction.LIKE, QuoteReaction.DISLIKE]:
        return JsonResponse(
            {"success": False, "error": "Invalid reaction type"}, status=400
        )

    user_uuid = get_or_create_user_uuid(request)

    reaction, created = QuoteReaction.objects.update_or_create(
        quote=quote, user_uuid=user_uuid, defaults={"type": reaction_type}
    )

    quote.refresh_from_db()

    response = JsonResponse(
        {
            "success": True,
            "reaction": reaction.type,
            "likes_count": quote.likes_count(),
            "dislikes_count": quote.dislikes_count(),
        }
    )

    return response


def quote(request: HttpRequest, quote_id: int):
    if request.method == "GET":
        return get_quote(request, quote_id)
    elif request.method == "DELETE":
        return delete_quote(request, quote_id)
    elif request.method == "POST":
        return add_quote(request)

    return JsonResponse({"success": False, "error": "Invalid HTTP method"}, status=405)


def delete_quote(request: HttpRequest, quote_id: int):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.delete()

    return JsonResponse({"success": True})


def add_quote(request: HttpRequest):
    data = json.loads(request.body.decode("utf-8"))

    text = data.get("text")
    source_id = data.get("source_id")
    attribution = data.get("attribution", None)
    weight = data.get("weight", 1)

    if not text or not source_id:
        return JsonResponse(
            {"success": False, "error": "Missing required fields"}, status=400
        )

    quote = Quote.objects.create(
        text=text, source_id=source_id, attribution=attribution, weight=weight
    )

    return JsonResponse({"success": True, "quote_id": quote.id})


def get_quote(request: HttpRequest, quote_id: int):
    quote = get_object_or_404(Quote, id=quote_id)

    quote_data = {
        "id": quote.id,
        "text": quote.text,
        "source": quote.source.name,
        "attribution": quote.attribution,
        "weight": quote.weight,
        "likes_count": quote.likes_count(),
        "dislikes_count": quote.dislikes_count(),
    }

    return JsonResponse({"success": True, "quote": quote_data})
