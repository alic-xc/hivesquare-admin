import base64

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from settings.forms import SlideShowForm, CategoryForm
from helpers.connector import data_connector, file_connector
from helpers.services import UserLoginRequiredMixin, CustomContextMixin, error_handler, history_pagination, get_request, \
    params_extracter, post_request, delete_request


class SlideShowView(UserLoginRequiredMixin, CustomContextMixin, generic.FormView):
    template_name = 'settings/slideshow.html'
    form_class = SlideShowForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        params = params_extracter(self.request)
        print(params)
        context['slideshows'] = get_request(self.request, '/slideshow')
        return context

    def form_valid(self, form):

        param = {'caption': form.cleaned_data['caption']}
        url = 'slideshow/'
        response = data_connector(self.request, url, param, 'post')
        if response['success']:
            param = {'image': (str(form.cleaned_data['image']), form.cleaned_data['image'])}
            url = 'slideshow/%s/' % response['data']['id']
            response = file_connector(self.request, url, param, 'patch')
            if response['success']:
                messages.success(self.request, "SlideShow uploaded successfully.")
            else:
                error_handler(self.request, response['data'])
                return super().form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('slideshow')


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


def delete_action(request, object_id, object_type):
    if object_type == 'category':
        url = 'category/%s/' % object_id
    elif object_type == 'sub-category':
        url = 'sub-category/%s/' % object_id
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

    else:
        return redirect('dashboard')