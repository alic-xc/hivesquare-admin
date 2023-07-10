from django import forms


class SlideShowForm(forms.Form):
    image = forms.ImageField(required=True)
    caption = forms.CharField(required=True)
    id = forms.UUIDField(required=False)


class AdsForm(forms.Form):
    image = forms.ImageField(required=True)
    caption = forms.CharField(required=True)
    link = forms.URLField(required=True)
    id = forms.UUIDField(required=False)


class BusinessCategoryForm(forms.Form):
    image = forms.ImageField(required=True)
    title = forms.CharField(required=True)
    id = forms.UUIDField(required=False)


class CategoryForm(forms.Form):
    image = forms.ImageField(required=True)
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    id = forms.UUIDField(required=False)


class SubCategoryForm(forms.Form):
    image = forms.ImageField(required=True)
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    category = forms.UUIDField(required=True)
    id = forms.UUIDField(required=False)