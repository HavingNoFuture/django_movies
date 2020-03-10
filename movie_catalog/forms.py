from django import forms

from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from movie_catalog.models import Reviews, Rating, RatingStars


class ReviewForm(forms.ModelForm):
    """Форма отзывов."""
    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ("name", "email", "text", "captcha")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={
                "class": "form-control border",
                "id": "contactcomment"
            })
        }


class RatingForm(forms.ModelForm):
    """Форма отзывов."""
    star = forms.ModelChoiceField(
        queryset=RatingStars.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)
