from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import FormView

from account.forms import LoginForm
from helpers.connector import data_connector
from helpers.services import error_handler, handle_next_page_redirection, UserLoginRequiredMixin, get_customers_list, \
    CustomContextMixin, get_user, get_dashboard, connect_analytics, get_date_values, get_request, patch_request, \
    post_request


class LoginView(generic.FormView):
    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        """ Intercept dispatch to check if there is active session"""
        try:
            """ Check if there is an active session """
            if self.request.session.get('staff_session_token', None):
                self.user = get_user(self.request)
                return redirect('dashboard')
            else:
                raise KeyError

        except KeyError:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        params = {
            'email': form.cleaned_data['username'],
            'password': form.cleaned_data['password'],
        }
        url = 'auth/login/'
        response = data_connector(self.request, url, params, 'post')

        if response['success']:
            self.request.session['staff_session_token'] = response['data']['access']
            return super().form_valid(form)

        else:
            try:
                error_handler(self.request, response['data'])
            except (TypeError, KeyError) as err:
                pass

        return super().form_invalid(form)

    def get_success_url(self):
        return handle_next_page_redirection(self.request)


class ProfileView(UserLoginRequiredMixin, CustomContextMixin, generic.TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['staff'] = context['user']
        context['personal'] = True
        return context


class DashboardView(UserLoginRequiredMixin, CustomContextMixin, generic.TemplateView):
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['dashboard'] = get_request(self.request, 'staff_dashboard/')
        if context['dashboard'].get('graph'):
            context['graph'] = generate_graph_data(context['dashboard']['graph'])
        return context


def search(request):
    try:
        q = request.GET.get('q', None)
        search_type = request.GET.get('type', None)
        fallbackurl = request.GET.get('fallbackurl', '')

        if search_type == 'transaction':
            return redirect('transaction', q)
        elif search_type == 'customer':
            return redirect('customer', q)
        else:
            raise Exception

    except Exception:
        if is_safe_url(fallbackurl, settings.ALLOWED_HOSTS):
            return redirect(reverse(fallbackurl))
        else:
            return redirect('dashboard')


def analytics(request):
    """  """
    # today = datetime.today().date().month

    sort_by = request.GET.get('sort_by', "month")
    from_date = request.GET.get('from_date', None)
    to_date = request.GET.get('to_date', None)
    from_date = str(from_date).replace('/', '-').strip(' ')
    to_date = str(to_date).replace('/', '-').strip(' ')
    user_id = request.GET.get('user_id', None)
    company_id = request.GET.get('merchant_id', None)
    driver_id = request.GET.get('rider_id', None)
    vehicle_id = request.GET.get('vehicle_id', None)
    query_params = "from_date=%s&to_date=%s" % (from_date, to_date)

    if vehicle_id:
        query_params += "&vehicle_id=%s&sort_by=%s" % (vehicle_id, sort_by)
    elif driver_id:
        query_params += "&rider_id=%s&sort_by=%s" % (driver_id, sort_by)
    elif company_id:
        query_params += "&company_id=%s&sort_by=%s" % (company_id, sort_by)
    else:
        query_params += "&user_id=%s" % user_id

    conn = connect_analytics(request, query_params)
    results = {}
    if not conn['success']:
        results['results'] = []
    else:
        results['results'] = conn['data']
        # if not user_id:
            # results['graph'] = generate_graph_data(conn['data']['graph_data'], sort_by)

    return JsonResponse(data=results, status=200)


def generate_graph_data(obj):

    dates = set()
    results = {
        'dates': [],
        'revenues': '',
        'earnings': ''
    }
    for item in obj['revenues']:
        print(item)
        try:
            dates.add(datetime.strptime(item['day'], '%Y-%m-%dT%H:%M:%SZ').date().strftime('%Y-%m-%d'))
        except Exception:
            dates.add(datetime.strptime(item['day'], '%Y-%m-%dT%H:%M:%S').date().strftime('%Y-%m-%d'))

    for item in obj['earnings']:
        try:
            dates.add(datetime.strptime(item['day'], '%Y-%m-%dT%H:%M:%SZ').date().strftime('%Y-%m-%d'))

        except Exception:
            dates.add(datetime.strptime(item['day'], '%Y-%m-%dT%H:%M:%S').date().strftime('%Y-%m-%d'))

    dates_list = sorted(dates)

    results['dates'] = dates_list
    results['revenues'] = get_date_values(date_list=dates_list, data=obj['revenues'])
    results['earnings'] = get_date_values(date_list=dates_list, data=obj['earnings'])

    try:
        get_date = datetime.strptime(dates_list[-1], '%Y-%m-%d')
    except:
        get_date = datetime.today().date()

    date = get_date + timedelta(days=1)

    results['dates'].append(date.strftime('%Y-%m-%d'))
    results['revenues'].append(0)
    results['earnings'].append(0)

    return results




def account_deletion(request, user_id, user_type):
    url = "account_deactivation/"
    conn = post_request(request, url, {"user_id": user_id})

    if conn['success']:
        messages.success(request, "Account deleted successfully")
    else:
        error_handler(request, conn['data'])

    return redirect(user_type)


def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    nxt = request.GET.get('next', '')
    return redirect(reverse('login') + "?next=" + nxt)
