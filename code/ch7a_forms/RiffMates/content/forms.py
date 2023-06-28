# RiffMates/content/forms.py
from django import forms


class CommentForm(forms.Form):
    name = forms.CharField()
    comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "6", "cols": "50"})
    )
