from django import forms

from quotes.models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["source", "text", "attribution", "weight"]

    text = forms.CharField(max_length=500, widget=forms.Textarea())
    weight = forms.IntegerField(min_value=1, max_value=100)
