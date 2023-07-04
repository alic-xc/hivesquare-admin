from django import forms


class SlideShowForm(forms.Form):
    image = forms.ImageField(required=True)
    caption = forms.CharField(required=True)

