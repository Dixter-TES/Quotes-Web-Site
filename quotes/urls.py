from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "api/quotes/<int:quote_id>/",
        views.quote,
        name="quote",
    ),
    path(
        "api/quotes/<int:quote_id>/react/",
        views.add_or_update_quote_reaction,
        name="reaction_quote",
    ),
    path("rating/", views.rating, name="rating"),
    path("editor/", views.editor, name="editor"),
    path("editor/<int:quote_id>/", views.editor, name="editor"),
]
