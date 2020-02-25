from django import forms

from movie_catalog.models import Reviews, Rating, RatingStars


class ReviewForm(forms.ModelForm):
    """Форма отзывов."""
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):
    """Форма отзывов."""
    star = forms.ModelChoiceField(
        queryset=RatingStars.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)
