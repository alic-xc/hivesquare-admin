from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from helpers.services import CustomContextMixin, get_customers_list, error_handler, \
    delete_customer_files, approve_customer_kyc, get_analytics, UserLoginRequiredMixin, get_request, SearchMixin, \
    patch_request, get_businesses_list


class BusinessView(UserLoginRequiredMixin, CustomContextMixin, SearchMixin, generic.TemplateView):
    template_name = 'business/businesses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        params = {}
        page = self.request.GET.get('page', '')
        params['page'] = page
        context['analytics'] = get_request(self.request, 'business_analytics/')
        context['businesses'] = get_businesses_list(self.request, params)
        print(context['businesses'])
        return context


class BusinessDetailsView(UserLoginRequiredMixin, CustomContextMixin, generic.TemplateView):
    template_name = 'business/business-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        business_id = self.kwargs['business_id']
        context['business_id'] = business_id
        context['analytics'] = get_request(self.request, 'business_analytic/?user=%s' % business_id)
        context['business'] = get_request(self.request, "business/%s/" % business_id)
        return context
