from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from helpers.services import CustomContextMixin, get_customers_list, error_handler, \
    delete_customer_files, approve_customer_kyc, get_analytics, UserLoginRequiredMixin, get_request, SearchMixin, \
    patch_request


class CustomersView(UserLoginRequiredMixin, CustomContextMixin, SearchMixin, generic.TemplateView):
    template_name = 'customers/customers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        params = {}
        page = self.request.GET.get('page', '')
        params['page'] = page
        context['analytics'] = get_request(self.request, 'customers_analytics/')
        context['customers'] = get_customers_list(self.request, params)
        return context


class CustomerDetailsView(UserLoginRequiredMixin, CustomContextMixin, generic.TemplateView):
    template_name = 'customers/customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_id = self.kwargs['user_id']
        context['user_id'] = user_id
        context['analytics'] = get_request(self.request, 'user_analytic/?user=%s' % user_id)
        context['customer'] = get_request(self.request, "accounts/%s/" % user_id)
        return context


def customer_kyc(request, user_id, action):
    params = {}
    if action == 'deactivate':
        params['is_active'] = False

    elif action == 'activate':
        params['is_active'] = True

    elif action == 'approve':
        params['access'] = True

    elif action == 'disapprove':
        params['access'] = False

    conn = patch_request(request, "accounts/%s/?user_type=user" % user_id, params)
    if conn['success']:
        messages.success(request, "Action performed successfully")
    else:
        error_handler(request, conn['data'])

    return redirect('customer', user_id)


def delete_file(request, user_id, image_id, remark):
    conn = delete_customer_files(request, user_id, image_id, remark)
    if conn['success']:
        messages.success(request, "Document deleted successfully")
    else:
        error_handler(request, conn['data'])
    return redirect('customer', user_id)