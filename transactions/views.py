from django.views import generic
from helpers.services import UserLoginRequiredMixin, SearchMixin, CustomContextMixin, get_request


class TransactionsListView(UserLoginRequiredMixin, CustomContextMixin, SearchMixin, generic.TemplateView):
    template_name = 'transactions/transactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['transactions'] = get_request(self.request, "wallet_funding/")
        return context


class WithdrawalListView(UserLoginRequiredMixin, CustomContextMixin, SearchMixin, generic.TemplateView):
    template_name = 'transactions/withdrawals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        params = "?"

        company_id = self.request.GET.get('company_id')
        if company_id:
            params += "company_id=%s" % company_id

        rider_id = self.request.GET.get('driver_id')
        if rider_id:
            params += "rider_id=%s" % rider_id

        context['withdrawals'] = get_request(self.request, "withdrawal_logs/%s" % params)
        return context


class WithdrawalDetailsView(UserLoginRequiredMixin, CustomContextMixin, SearchMixin, generic.TemplateView):
    template_name = 'transactions/withdrawal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['withdrawal'] = get_request(self.request, "")
        return context


class EarningListView(UserLoginRequiredMixin, CustomContextMixin, generic.TemplateView):
    template_name = 'transactions/earning.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['earnings'] = get_request(self.request, "patch_earnings/")
        return context