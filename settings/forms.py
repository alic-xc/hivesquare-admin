from django import forms


class SlideShowForm(forms.Form):
    image = forms.ImageField(required=True)
    caption = forms.CharField(required=True)


class CategoryForm(forms.Form):
    image = forms.ImageField(required=True)
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)