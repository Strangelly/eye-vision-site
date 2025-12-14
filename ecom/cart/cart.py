from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')


        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'price': str(product.sale_price if product.is_sale else product.price),
                'quantity': quantity
            }

        self.session.modified = True


    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.session.modified = True


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_cart_items(self):
        items = []
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            pid = str(product.id)
            quantity = self.cart[pid]['quantity']
            price = float(self.cart[pid]['price'])
            total = quantity * price

            items.append({
                "product": product,
                "quantity": quantity,
                "price": price,
                "total": total
            })

        return items

    #calculate grand total
    def get_total_price(self):
        return sum(
            item['quantity'] * float(item['price']) 
            for item in self.cart.values()
        )

