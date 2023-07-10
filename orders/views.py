from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from helpers.services import CustomContextMixin, get_customers_list, error_handler, \
    delete_customer_files, approve_customer_kyc, get_analytics, UserLoginRequiredMixin, get_request, SearchMixin, \
    patch_request, params_extracter


class OrdersView(UserLoginRequiredMixin, CustomContextMixin, SearchMixin, generic.TemplateView):
    template_name = 'orders/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        param = params_extracter(self.request)
        context['orders'] = get_request(self.request, 'order/?' + param['url'])
        context['analytics'] = get_request(self.request, 'orders_analytics/')
        context['extra'] = param['config']
        return context


class OrderDetailsView(UserLoginRequiredMixin, CustomContextMixin, generic.TemplateView):
    template_name = 'orders/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        order_id = self.kwargs['order_id']
        context['order_id'] = order_id
        context['order'] = get_request(self.request, "order/%s/?extra=yes" % order_id)
        context['analytics'] = get_request(self.request, 'orders_analytics/?order_id=%s' % order_id)
        print(context['analytics'])
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