from django.conf import settings

from djstripe.models import Customer, StripeCard
import stripe
stripe.api_key = getattr(settings,"STRIPE_SECRET_KEY",None)

from drop.exceptions import PaymentError
from .abstract import PaymentBackend

class Stripe(PaymentBackend):
  name = "stripe"
  def charge(self,order,request):
    metadata = {"order_id": order.id}
    for i,item in enumerate(order.items.all()):
      metadata['item_%s'%i] = str(item.product)
      metadata['quantity_%s'%i] = item.quantity
      metadata['price_%s'%i] = item.line_total
    kwargs = {
      'amount': int(float(request.POST['total'])*100), # Amount in cents
      'source': request.POST['token'],
      'currency': "usd",
      'description': "Payment for order #%s"%order.id,
      'metadata': metadata,
    }
    customer = None
    card = None
    user = order.user
    if user:
      kwargs['customer'] = customer = Customer.get_or_create(user)[0]
      token = kwargs.pop('source')
    try:
      # both these could cause cards to be declines, so they both need to be in here
      if customer:
        card = customer.add_card(token)
      charge = stripe.Charge.create(**kwargs)
    except stripe.error.CardError,e:
      raise PaymentError(e)
    if card:
      card.remove()
  def refund(self,transaction_id):
    #! TODO needs error catching
    return stripe.Refund.create(charge=transaction_id).id
