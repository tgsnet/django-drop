from django.conf import settings
from djstripe.models import Customer, StripeCard
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from drop.exceptions import PaymentError
from .abstract import PaymentBackend

class Stripe(PaymentBackend):
  name = "stripe"
  def charge(self,order,request):
    kwargs = {
      'amount': int(order.order_total*100), # Amount in cents
      'source': request.POST['token'],
      'currency': "usd",
      'description': "Payment for order #%s"%order.id,
      'metadata': {"order_id": order.id},
    }
    customer = None
    card = None
    if order.user:
      kwargs['customer'] = customer = Customer.get_or_create(order.user)[0]
      token = kwargs.pop('source')
      card = customer.add_card(token)
    try:
      charge = stripe.Charge.create(**kwargs)
    except stripe.error.CardError,e:
      raise PaymentError(e)
    print card
    if card:
      card.remove()
  def refund(self,transaction_id):
    #! TODO needs error catching
    return stripe.Refund.create(charge=transaction_id).id
