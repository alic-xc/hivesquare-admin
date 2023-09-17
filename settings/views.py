import base64

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from settings.forms import SlideShowForm, CategoryForm, SubCategoryForm, BusinessCategoryForm, AdsForm, SubscriptionForm
from helpers.connector import data_connector, file_connector
from helpers.services import UserLoginRequiredMixin, CustomContextMixin, error_handler, history_pagination, get_request, \
    params_extracter, post_request, delete_request


class SlideShowView(UserLoginRequiredMixin, CustomContextMixin, generic.FormView):
    template_name = 'account/slideshow.html'
    form_class = SlideShowForm

    def get_success_url(self):
        return reverse('slideshow')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['slideshows'] = get_request(self.request, 'slideshows/')
        return context

    def form_valid(self, form):
        try:
            data = form.cleaned_data
            image = base64.b64encode(data['image'].read()).decode('utf-8')
            params = {
                'caption': data['caption'],
                'image':  image
            }
            url = str('slideshows/')
            response = post_request(self.request, url, params)
            if response['success']:
                messages.success(self.request, "SlideShow created successfully.")
            else:
                error_handler(self.request, response['data'])
                return super().form_invalid(form)

        except KeyError as err:
            messages.error(self.request, "System error. Please, try again after sometime")
            return super().form_invalid(form)

        return super().form_valid(form)


class AdsView(UserLoginRequiredMixin, CustomContextMixin, generic.FormView):
    template_name = 'account/ads.html'
    form_class = AdsForm

    def get_success_url(self):
        return reverse('ads')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['ads'] = get_request(self.request, 'ads/')
        return context

    def form_valid(self, form):
        try:
            data = form.cleaned_data
            image = base64.b64encode(data['image'].read()).decode('utf-8')
            params = {
                'caption': data['caption'],
                'image':  image,
                'link': data['link']
            }
            url = str('ads/')
            response = post_request(self.request, url, params)
            if response['success']:
                messages.success(self.request, "Ad created successfully.")
            else:
                error_handler(self.request, response['data'])
                return super().form_invalid(form)

        except KeyError as err:
            messages.error(self.request, "System error. Please, try again after sometime")
            return super().form_invalid(form)

        return super().form_valid(form)


class CategoryView(UserLoginRequiredMixin, CustomContextMixin, generic.FormView):
    template_name = 'settings/category.html'
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        param = params_extracter(self.request)
        context['categories'] = get_request(self.request, 'category/?' + param['url'])
        context['extra'] = param['config']
        return context

    def form_valid(self, form):

        url = 'category/'
        data = form.cleaned_data
        image = base64.b64encode(data['image'].read()).decode('utf-8')
        params = {
            "name": data['title'],
            "description": data['description'],
            "image": image
        }
        response = post_request(self.request, url, params)
        if response['success']:
            messages.success(self.request, "Category uploaded successfully.")

        else:
            error_handler(self.request, response['data'])
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('category')


class SubCategoryView(UserLoginRequiredMixin, CustomContextMixin, generic.FormView):
    template_name = 'settings/sub-category.html'
    form_class = SubCategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        param = params_extracter(self.request)
        context['categories'] = get_request(self.request, 'category/?' + param['url'])
        context['sub_categories'] = get_request(self.request, 'sub-category/?' + param['url'])
        context['extra'] = param['config']
        return context

    def form_valid(self, form):
        url = 'sub-category/'
        data = form.cleaned_data
        image = base64.b64encode(data['image'].read()).decode('utf-8')
        params = {
            "name": data['title'],
            "category": str(data['category']),
            "description": data['description'],
            "image": image
        }
        response = post_request(self.request, url, params)
        if response['success']:
            messages.success(self.request, "Sub-Category uploaded successfully.")

        else:
            error_handler(self.request, response['data'])
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('sub-category')


class BusinessCategoryView(UserLoginRequiredMixin, CustomContextMixin, generic.FormView):
    template_name = 'settings/business-category.html'
    form_class = BusinessCategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        param = params_extracter(self.request)
        context['categories'] = get_request(self.request, 'business_category/?' + param['url'])
        context['extra'] = param['config']
        return context

    def form_valid(self, form):

        url = 'business_category/'
        data = form.cleaned_data
        image = base64.b64encode(data['image'].read()).decode('utf-8')
        params = {
            "name": data['title'],
            "image": image
        }
        response = post_request(self.request, url, params)
        if response['success']:
            messages.success(self.request, "Business Category uploaded successfully.")

        else:
            error_handler(self.request, response['data'])
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('business-category')


class SubscriptionView(UserLoginRequiredMixin, generic.FormView):
    template_name = 'settings/subscription.html'
    form_class = SubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['subscriptions'] = get_request(self.request, 'subscription/')
        return context

    def form_valid(self, form):

        url = 'subscription/'
        data = form.cleaned_data
        params = {
            "title": data['title'],
            "type": "premium",
            "amount": str(data["amount"]),
            "discount_1st_month": str(data["discount_1st_month"]),
            "discount_3rd_month": str(data["discount_3rd_month"]),
            "discount_12th_month": str(data["discount_12th_month"]),
            "available_features": {"features": self.request.POST.get('features')},
            "total_distance":  str(data['distance']),
            "total_businesses":  data['store'],
        }

        response = post_request(self.request, url, params)
        if response['success']:
            messages.success(self.request, "Subscription created successfully.")

        else:
            error_handler(self.request, response['data'])
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('subscription')


def delete_action(request, object_id, object_type):
    if object_type == 'category':
        url = 'category/%s/' % object_id

    elif object_type == 'sub-category':
        url = 'sub-category/%s/' % object_id

    elif object_type == 'business_category':
        url = 'business-category/%s/' % object_id

    elif object_type == 'slideshow':
        url = 'slideshows/%s/' % object_id

    elif object_type == 'ads':
        url = 'ads/%s/' % object_id

    else:
        return redirect('dashboard')

    conn = delete_request(request, url, {})
    if conn['success']:
        messages.success(request, "%s deleted successfully" % object_type)
    else:
        error_handler(request, conn['data'])

    if object_type == 'category':
        return redirect('category')

    elif object_type == 'sub-category':
        return redirect('sub-category')

    elif object_type == 'business_category':
        return redirect('business-category')

    elif object_type == 'slideshow':
        return redirect('slideshow')

    elif object_type == 'ads':
        return redirect('ads')

    else:
        return redirect('dashboard')