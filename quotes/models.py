from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError


class Quote(models.Model):
    source = models.CharField(max_length=150)

    text = models.CharField(max_length=500, unique=True)
    attribution = models.CharField(max_length=150, null=True)
    weight = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    
    def likes_count(self):
        return self.reactions.filter(type=QuoteReaction.LIKE).count()
    
    def dislikes_count(self):
         return self.reactions.filter(type=QuoteReaction.DISLIKE).count()
     
    def clean(self):
        if Quote.objects.filter(source=self.source).exclude(id=self.id).count() >= 3:
            raise ValidationError(f'У источника "{self.source}" уже есть 3 цитаты')
     
    def __str__(self):
        return f"{self.source} | {self.text} | {self.attribution}"


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
    
    def __str__(self):
        return f"{self.type} | {self.quote.id}:{self.quote.text}"


class Statistics(models.Model):
    total_views = models.PositiveIntegerField(default=0)
