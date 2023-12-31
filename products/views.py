from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from helpers.services import CustomContextMixin, get_customers_list, error_handler, \
    delete_customer_files, approve_customer_kyc, get_analytics, UserLoginRequiredMixin, get_request, SearchMixin, \
    patch_request, params_extracter, post_request


class ProductsView(UserLoginRequiredMixin, CustomContextMixin, SearchMixin, generic.TemplateView):
    template_name = 'products/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        param = params_extracter(self.request)
        context['products'] = get_request(self.request, 'product/?' + param['url'])
        context['analytics'] = get_request(self.request, 'product_analytics/')
        context['extra'] = param['config']
        return context


class ProductDetailsView(UserLoginRequiredMixin, CustomContextMixin, generic.TemplateView):
    template_name = 'products/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_id = self.kwargs['product_id']
        context['product_id'] = user_id
        context['analytics'] = get_request(self.request, 'analytic/?user=%s' % user_id)
        context['product'] = get_request(self.request, "product/%s/" % user_id)
        return context


def product_kyc(request, product_id, action):
    params = {}
    if action == 'deactivate':
        params['is_active'] = 'deactivate'

    elif action == 'activate':
        params['is_active'] = 'activate'

    elif action == 'publish':
        params['is_publish'] = 'publish'

    elif action == 'unpublish':
        params['is_publish'] = 'unpublish'

    conn = post_request(request, "staff/product/%s" % product_id, params)
    if conn['success']:
        messages.success(request, "Action performed successfully")

    else:
        error_handler(request, conn['data'])

    return redirect('product', product_id)


def delete_file(request, user_id, image_id, remark):
    conn = delete_customer_files(request, user_id, image_id, remark)
    if conn['success']:
        messages.success(request, "Document deleted successfully")
    else:
        error_handler(request, conn['data'])
    return redirect('customer', user_id)