from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from helpers.services import CustomContextMixin, get_vendors_list, error_handler, \
    delete_customer_files, approve_customer_kyc, UserLoginRequiredMixin, get_request, SearchMixin


class VendorView(UserLoginRequiredMixin, CustomContextMixin, SearchMixin, generic.TemplateView):
    template_name = 'vendor/vendors.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        params = {}
        page = self.request.GET.get('page', '')
        params['page'] = page
        context['analytics'] = get_request(self.request, 'customers_analytics/')
        context['vendors'] = get_vendors_list(self.request, params)
        return context


class VendorDetailsView(UserLoginRequiredMixin, CustomContextMixin, generic.TemplateView):
    template_name = 'vendor/vendor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_id = self.kwargs['user_id']
        context['user_id'] = user_id
        context['analytics'] = get_request(self.request, 'vendor_analytic/?vendor_id=%s' % user_id)
        context['vendor'] = get_request(self.request, "accounts/%s/?user_type=vendor" % user_id)
        context['user_bank'] = get_request(self.request, "user_banks/?user_id=%s" % user_id)
        return context


def vendor_kyc(request, user_id, action):
    conn = approve_customer_kyc(request, user_id, action)
    msg = {'activate': 'activated', 'deactivate': 'deactivated', 'approve': 'approved', 'disapprove': 'disapproved'}
    if conn['success']:
        messages.success(request, "Customer %s successfully" % msg[action])
    else:
        error_handler(request, conn['data'])
    return redirect('vendor', user_id)






def delete_file(request, user_id, image_id, remark):
    conn = delete_customer_files(request, user_id, image_id, remark)
    if conn['success']:
        messages.success(request, "Document deleted successfully")
    else:
        error_handler(request, conn['data'])
    return redirect('customer', user_id)