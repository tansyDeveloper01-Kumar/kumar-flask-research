from .apiActLkpTaxType import clsLkpActTaxType
from .apiActLkpPaymentTerms import clsActLkpPaymentTerms


def fn_lkp_act_initialize_routes(api):
    api.add_resource(clsLkpActTaxType, '/api/lkp/v1/tax-type')
    api.add_resource(clsActLkpPaymentTerms, '/api/lkp/v1/payment-terms')