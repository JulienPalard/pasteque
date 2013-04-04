from django.forms import ModelForm
from models import Paste, Language


class LanguageForm(ModelForm):
    """Language model form."""
    class Meta:
        model = Language


class PasteForm(ModelForm):
    """Paste model form."""
    class Meta:
        model = Paste

    def save(self, commit=True):
        """Overwrites save method."""
        paste = super(PasteForm, self).save(commit=False)
        paste.compute_size()
        if not self.cleaned_data['title']:
            paste.title = 'no title'
        if self.cleaned_data['password']:
            paste.set_password(self.cleaned_data['password'])
        if commit:
            paste.save()
        return paste
