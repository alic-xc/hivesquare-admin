from django.contrib import messages
from django.urls import reverse
from django.views import generic
from settings.forms import SlideShowForm
from helpers.connector import data_connector, file_connector
from helpers.services import UserLoginRequiredMixin, CustomContextMixin, error_handler, history_pagination, get_request, \
    params_extracter


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

