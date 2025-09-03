from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Source(models.Model):
    name = models.CharField(max_length=50)


class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    text = models.CharField(max_length=500, unique=True)
    attribution = models.CharField(max_length=150, null=True)
    weight = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])


class QuoteReaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"
    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]
    
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="reactions")

    type = models.CharField(max_length=10, choices=REACTION_CHOICES, null=True)
    user_uuid = models.CharField(max_length=36)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    unique_quote_user_uuid = models.UniqueConstraint(
        "quote", "user_uuid", name="unique_quote_user_uuid"
    )


class Statistics(models.Model):
    total_views = models.PositiveIntegerField(default=0)
