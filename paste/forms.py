from webtools import settings
from django import forms
from django.forms import ModelForm, CharField
from .models import Paste, Language, EXPIRE_CHOICES


class PasteForm(ModelForm):
    """Paste model form."""

    content = CharField(
        max_length=settings.PASTE["max_characters"], strip=False, widget=forms.Textarea
    )

    class Meta:
        model = Paste
        fields = [
            "language",
            "title",
            "password",
            "content",
            "lifetime",
            "lifecount",
            "private",
        ]

    def save(self, commit=True):
        """Overwrites save method."""
        paste = super(PasteForm, self).save(commit=False)
        paste.compute_size()
        if not self.cleaned_data["title"]:
            paste.title = "no title"
        if self.cleaned_data["password"]:
            paste.set_password(self.cleaned_data["password"])
        if commit:
            paste.save()
        return paste
