from datetime import datetime

from django.conf import settings
from django.contrib import messages
from functools import wraps

from django.shortcuts import redirect
from django.urls import  reverse_lazy

from .connector import data_connector, file_download_connector


class UserLoginRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        try:
            var = request.session['staff_session_token']
            print(var)
            conn = get_user(request)
            print(conn)
            if conn:
                self.user = conn
                return super().dispatch(request, *args, **kwargs)
            else:
                del request.session['staff_session_token']
                raise KeyError

        except KeyError as err:
            return redirect('login')


class CustomContextMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.user
        return context


class SearchMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        search_value = self.request.GET.get('search_value', None)
        search_type = self.request.GET.get('search_type', None)
        if search_type and search_type:
            url_params = "?search_value=%s&search_type=%s" % (search_value, search_type)
            context['search'] = get_request(self.request, 'search/%s'%url_params)
            context['search_value'] = search_value
            context['search_type'] = search_type

        return context


def get_user(request, no_msg=None):
    url = 'users/'
    response = data_connector(request, url, None, 'get')
    print(response)
    if response['success']:
        return response['data']
    return None


def get_sme(request, query):
    """ Get all sme """
    url = 'company/'
    if query:
        url = 'company/%s' % query
    return data_connector(request, url, None, 'get')


def get_merchant(request, sme_id):
    url = 'company/%s/' % sme_id
    response = data_connector(request, url, None, 'get')
    return response


def get_user_extra(request):
    url = 'user/settings'
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def get_services(request, query=None):

    url = "services/"
    if query:
        url += query

    return data_connector(request, url, None, 'get')


def get_service(request, service_id):
    url = 'services/%s' % service_id
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return []


def get_drivers(request, query=None):
    url = 'rider/'
    if query:
        url = 'rider/%s' % query
    print(url)
    return data_connector(request, url, None, 'get')


def connect_service_category(request):
    """ """
    url = 'service_category/'
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return []


def connect_save_service(request, data):
    url = 'create_delivery/'
    params = data
    response = data_connector(request, url, params, 'post')
    return response


def connect_calculator(request, distance, duration ):
    url = 'fare_calculator/?est_dist=%s&est_time=%s' %(distance, duration)
    response = data_connector(request, url, None, 'get')
    return response


def get_vendors(request, query):
    url = 'users/%s' % query
    return data_connector(request, url, None, 'get')


def get_payouts(request, query=None):
    url = 'withdraw_log/'
    if query:
        url = 'withdraw_log/%s' % query

    return data_connector(request, url, None, 'get')


def get_wallets(request, query=None):
    url = 'wallet_log/'
    if query:
        url = 'wallet_log/%s' % query

    return data_connector(request, url, None, 'get')


def get_remittance(request, query=None):
    url = 'pay_patch/'
    if query:
        url = 'pay_patch/%s' % query

    return data_connector(request, url, None, 'get')


def get_driver(request, driver_id):
    url = 'rider/%s' % driver_id
    response = data_connector(request, url, None, 'get')
    return response


def get_driver_action(request, params):
    url = 'user_access/'
    response = data_connector(request, url, params, 'patch')
    return response


def get_banks(request, data=None):
    url = 'banks/'
    return get_list_api(request, url, data)


def get_dashboard(request):
    url = 'staff_dashboard/'
    response = data_connector(request, url, None, 'get')
    return response


def connect_analytics(request, query):
    """ """
    url = 'analytics?%s' % query
    response = data_connector(request, url, None, 'get')
    return response


def connect_user_registration(request, params):
    """ """
    url = '/users/'
    response = data_connector(request, url, params, 'post')
    return response


def get_date_values(**kwargs):
    results = []
    for item in kwargs['date_list']:
        data = 0
        for itemx in kwargs['data']:
            date_str = datetime.strptime(item, '%Y-%m-%d').date()
            try:
                converted_date = datetime.strptime(itemx['day'], '%Y-%m-%dT%H:%M:%SZ').date()
            except ValueError:
                converted_date = datetime.strptime(itemx['day'], '%Y-%m-%dT%H:%M:%S').date()

            if date_str == converted_date:
                data = itemx['amount']
                break;

        results.append(data)

    return results


def get_screenshots(request, data=None):
    url = 'screenshots/'
    return get_list_api(request, url, data)


def get_screenshot(request, driver_id):
    url = 'screenshots/%s' % driver_id
    response = data_connector(request, url, None, 'get')
    return response


def get_initial_history(request, data=None):
    url = 'staff/initial/log/'
    return get_list_api(request, url, data)


def get_revenue_history(request, currency_id, data=None):
    url = 'staff/revenue/?currency=%s' % currency_id
    return get_list_api(request, url, data)


def get_transaction(request, token):
    if token:
        url = 'staff/transaction/%s/' % token
        response = data_connector(request, url, None, 'get')
        if response['success']:
            return response['data']
    return {}


def get_staff_detail(request, id):
    if id:
        url = 'staff/customers/%s/' % id
        response = data_connector(request, url, None, 'get')
        if response['success']:
            return response['data']
    return {}


def get_account_statements(request, data=None):
    url = 'transaction/statement/'
    if not data:
        response = data_connector(request, url, None, 'get')
    else:
        response = data_connector(request, url, data, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def download_merchant_statements(request, data):
    url = 'transaction/statement/download/'
    response = file_download_connector(request, url, data, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def get_receipt(request, token):
    url = 'transaction/receipts/'
    response = file_download_connector(request, url, {'token': token}, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def get_custom_users(request, query, uuid):
    if query == 'sub_entity':
        url = 'customers/?sub_entity=%s' % uuid
    else:
        url = 'customers/?unit=%s' % uuid
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def get_user_by_username(request, username):
    url = 'customers/?user=%s' % username
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def get_transaction_by_id(request, deposit_id):
    url = 'deposit/%s/' % deposit_id
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def get_withdraw_by_id(request, withdraw_id):
    url = 'withdraw/%s/' % withdraw_id
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def get_bank(request, bank_id=None):
    if not bank_id:
        url = 'user/bank/'
    else:
        url = 'user/bank/%s/' % bank_id
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def user_login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            var = request.session['session_token']
            return function(request, *args, **kwargs)
        except KeyError as err:
            messages.error(request, 'We noticed an unusual activity with your account.'
                                    ' Please login again to validate account')
            from account.views import logout
            return logout(request)

    return wrap


def error_handler(request, errors):

    if type(errors) == str:
        messages.error(request, errors)

    elif type(errors) == dict:
        for error in errors.keys():
            if type(errors[error]) == list:
                for item in errors[error]:
                    print(item)
                    messages.error(request, item)
            else:
                messages.error(request, errors[error])

    elif type(errors) == list:
        for error in errors:
            if type(error) == dict:
                for item in error.keys():
                    messages.error(request, error[item])
            else:
                messages.error(request, error)
    else:
        messages.error(request, "System error, please try again.")
    return errors


def handle_next_page_redirection(request):
    try:
        user = get_user(request, True)
        url = request.GET.get('next', '')
        if is_safe_url(url, settings.ALLOWED_HOSTS):
            return url

    except Exception as err:
        pass

    return reverse_lazy('dashboard')


def handle_pagination(request, user_id=None, feature_type=None):
    """  """
    query_params = {'page': request.GET.get('page', 1)}
    url_query = "?page=%s" % query_params['page']

    # filter by status
    status_list = request.GET.getlist('status', '')
    if status_list:
        url_arr = ''
        for status in status_list:
            url_arr += "&status=%s" % status

        url_query += url_arr

    # order by
    order_by = request.GET.get('order_by', 'date_joined')
    if order_by:
        url_query += "&order_by=%s" % order_by

    # filter by date range
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    if start_date and end_date:
        url_query += "&date_range=%s - %s" %(start_date, end_date)

    data = {'page_num': query_params['page']}

    # feature type
    if feature_type == 'sme':
        results = get_sme(request, url_query)
        data['sme'] = results

    elif feature_type == 'drivers':
        if user_id:
            url_query += "&company_id=" + user_id
        results = get_drivers(request, url_query)
        data['drivers'] = results

    elif feature_type == 'services' or feature_type == 'awaiting_services':

        if feature_type == 'services':
            # filter by service status
            if not request.GET.getlist('services_status', None):
                services_status = ['pending', 'arrived', 'accepted', 'in-transit', 'completed']
            else:
                services_status = request.GET.getlist('services_status')

            url_arr = ''
            url_arr += "&sort_by=%s" % ','.join(services_status)
            url_query += url_arr

        else:
            url_query += "&sort_by=queue"

        # filter by vehicle, driver or merchant.
        if request.GET.get('service_type') == 'vehicle':
            vehicle_id = request.GET.get('vehicle_id', '')
            url_query += "&vehicle_id=%s&service_type=vehicle" % vehicle_id

        elif request.GET.get('service_type') == 'rider':
            driver_id = request.GET.get('driver_id', '')
            url_query += "&rider_id=%s&service_type=driver" % driver_id

        elif request.GET.get('service_type') == 'merchant':
            merchant_id = request.GET.get('company_id', '')
            url_query += "&company_id=%s&service_type=merchant" % merchant_id

        results = get_services(request, url_query)
        data['services'] = results

    elif feature_type == 'payout':
        if user_id:
            url_query += "&driver_id=" + user_id
        results = get_payouts(request, url_query)
        data['payout'] = results

    elif feature_type == 'remittance':
        if user_id:
            url_query += "&driver_id=" + user_id
        results = get_remittance(request, url_query)
        data['remittance'] = results

    elif feature_type == 'payout':
        if user_id:
            url_query += "&driver_id=" + user_id
        results = get_payouts(request, url_query)
        data['remittance'] = results

    elif feature_type == 'wallet':
        if user_id:
            url_query += "&driver_id=" + user_id
        results = get_wallets(request, url_query)
        data['wallet'] = results

    elif feature_type == 'vendor':
        url_query += "&sort_by=vendor"
        results = get_vendors(request, url_query)
        data['vendors'] = results

    return data


def get_promo_codes(request, data=None):
    url = 'promotions/'
    return get_list_api(request, url, data)


def get_customers_list(request, data=None):
    url = 'accounts/?user_type=user'
    return get_list_api(request, url, data)


def get_vendors_list(request, data=None):
    url = 'accounts/?user_type=vendor'
    return get_list_api(request, url, data)


def get_customers_filtered(request, data=None):
    url = 'staff/customer/sort/?filter_by=is_active'
    return get_list_api(request, url, data)


def get_businesses_list(request, data=None):
    url = 'business/'
    return get_list_api(request, url, data)


def customer_counter(request):
    url = 'staff/customer/count/'
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def entity_counter(request, acc_no):
    url = 'staff/entity/details/?account_no=%s' % acc_no
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def get_staff_list(request, data=None):
    url = 'users/?sort_by=all'
    return get_list_api(request, url, data)


def get_list_api(request, url, data=None):
    url = url
    try:
        if data['page']:
            if url.find("?") > 1:
                url += "&"
            else:
                url += "?"
            url = url + "page=" + data['page']

    except Exception:
        pass

    if not data or len(data) == 1:
        response = data_connector(request, url, data, 'get')
    else:
        response = data_connector(request, url, data, 'get')

    if response['success']:
        return response['data']

    else:
        return {}




def phone_formatter(phone):
    """ Validate user phone number """

    if phone.startswith('0'):
        new_phone = phone[1:]
        return "{0}{1}".format('+234', new_phone)
    elif not phone.startswith('+') and phone.startswith('234'):
        return "{0}{1}".format('+', phone)
    elif not phone.startswith('+234') or not phone.startswith('234'):
        return "{0}{1}".format('+234', phone)
    else:
        return phone


def get_analytics(request, user_id):
    url = 'user_analytics/?user_id=%s' % user_id
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']
    else:
        return {}


def delete_customer_files(request, customer_id, image_id, remark):
    url = 'user_docs/?id=%s&image_id=%s&remark=%s' % (customer_id, image_id, remark)
    response = data_connector(request, url, None, 'delete')
    return response


def request_delete_loan_type(request, loan_type_id):
    url = 'loan_setup/%s' % loan_type_id
    response = data_connector(request, url, None, 'delete')
    return response


def request_delete_banks(request, bank_id):
    url = 'banks/%s' % bank_id
    response = data_connector(request, url, None, 'delete')
    return response


def request_delete_customer_files(request, loan_id, image_id):
    url = '/loan_docs/%s?file_id=%s' % (loan_id, image_id)
    response = data_connector(request, url, None, 'delete')
    return response


def request_delete_savings_type(request, saving_type_id):
    url = 'savings_setup/%s' % saving_type_id
    response = data_connector(request, url, None, 'delete')
    return response


def approve_customer_kyc(request, customer_id, action):
    url = 'user_action/?user_id=%s&action=%s' % (customer_id, action)
    response = data_connector(request, url, None, 'patch')
    return response


def history_pagination(query):
    """ Extract pagination from api """
    try:
        get_prev_link = query['previous'].split('?')[-1] if query[
            'previous'] else None  # Extract query params from next link
        get_next_link = query['next'].split('?')[-1] if query['next'] else None  # Extract query params from prev link
    except Exception:
        get_next_link = ''
        get_prev_link = ''

    return {
        'next': get_next_link,
        'prev': get_prev_link,
    }


def get_request(request, url):
    response = data_connector(request, url, None, 'get')
    if response['success']:
        return response['data']

    else:
        return {"error": True, "data": response['data']}


def post_request(request, url, params):
    response = data_connector(request, url, params, 'post')
    return response


def patch_request(request, url, params):
    response = data_connector(request, url, params, 'patch')
    return response