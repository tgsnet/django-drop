#! TODO Depracated. From django-shop, not used in drop ccc 11/16

# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from drop.util.decorators import on_method, drop_login_required, order_required


class PayOnDeliveryBackend(object):

    backend_name = "Pay On Delivery"
    backend_verbose_name = _("Pay On Delivery")
    url_namespace = "pay-on-delivery"

    def __init__(self, drop):
        self.drop = drop
        # This is the drop reference, it allows this backend to interact with
        # it in a tidy way (look ma', no imports!)

    @on_method(drop_login_required)
    @on_method(order_required)
    def simple_view(self, request):
        """
        This simple view does nothing but record the "payment" as being
        complete since we trust the delivery guy to collect money, and redirect
        to the success page. This is the most simple case.
        """
        # Get the order object
        the_order = self.drop.get_order(request)
        # Let's mark this as being complete for the full sum in our database
        # Set it as paid (it needs to be paid to the delivery guy, we assume
        # he does his job properly)
        self.drop.confirm_payment(
            the_order, self.drop.get_order_total(the_order), "None",
            self.backend_name)
        return HttpResponseRedirect(self.drop.get_finished_url())

    def get_urls(self):
        urlpatterns = [
            url(r'^$', self.simple_view, name='pay-on-delivery'),
        ]
        return urlpatterns
