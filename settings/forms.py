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


class SubscriptionForm(forms.Form):
    title = forms.CharField(required=True)
    distance = forms.DecimalField(required=True)
    store = forms.IntegerField(required=True)
    amount = forms.DecimalField(required=True)
    discount_1st_month = forms.DecimalField(required=True)
    discount_3rd_month = forms.DecimalField(required=True)
    discount_12th_month = forms.DecimalField(required=True)

