(function() {
  uR.schema.fields.amount = { type: 'number' };
  uR.schema.fields.delivery_date = { type: 'date' };
  uR.schema.fields.recipient_email = { type: 'email' };
  uR.drop._addToCart['giftcard.giftcardproduct'] = function(data) {
    uR.alertElement('purchase-giftcard',data);
  }
})();

<purchase-giftcard>
  <div class={ theme.outer }>
    <div class={ theme.header }><h3>Purchase a gift card</h3></div>
    <div class={ theme.content }>
      <ur-form schema={ product.extra_fields } success_text="Add to Cart" initial={ initial }></ur-form>
    </div>
  </div>

  var self = this;
  this.product = this.opts.product;
  this.initial = { }
  if (window.moment) { this.initial.delivery_date = window.moment().format("YYYY-MM-DD"); }
  if (uR.auth.user) {
    this.initial.recipient_name = uR.auth.user.username;
    this.initial.recipient_email = uR.auth.user.email;
  };
  if (uR.drop.product_on_page) { this.initial.amount = uR.drop.product_on_page.unit_price }
  this.submit = function(ur_form) {
    data = ur_form.getData();
    uR.drop.saveCartItem(self.product.id,data.amount,self,data)
  }
  this.add_successful = function() {
    self.unmount();
    uR.drop.openCart();
  }
</purchase-giftcard>
