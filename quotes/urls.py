from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "api/quote/<int:quote_id>/reactions/",
        views.add_or_update_quote_reaction,
        name="reaction_quote",
    ),
]
