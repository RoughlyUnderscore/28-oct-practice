import os


TAX = float(os.getenv("TAX_PERCENTAGE") or "13") + 1 # convert to total


class Product:
  def __init__(self, price: float, amount_available: int, category: str, sale: float = 0.0):
    self.price = price
    self.amount_available = amount_available
    self.category = category
    self.sale = sale
  
  def get_price(self):
    return self.price * (1 - self.sale)
  
  def set_sale(self, sale: float):
    self.sale = sale
  
  def remove_sale(self):
    self.sale = 0


class Store:
  def __init__(self):
    self._products = {}
  
  def reserve_product(self, product: Product, amount: int):
    total = self._products[product]
    if amount > total:
      raise ValueError("Not enough in stock")
    else:
      self._products[product] = total - amount
  
  def add_product(self, product: Product, amount: int = 1):
    if product in self._products:
      self._products[product] += amount
    else:
      self._products[product] = amount


store = Store()
# initialize and add some products... idk i can't be bothered sorry


class Order:
  def __init__(self):
    self.items = {}
  
  def checkout(self):
    return sum(
      amount * product.get_price() for (product, amount) in self.items.items()
      ) * (TAX / 100)


class ShoppingCart:
  def __init__(self):
    self._items = {}
  
  def add_item(self, product: Product, quantity: int = 1):
    store.reserve_product(product, quantity)
    if product in self._items.keys():
      self._items[product] += quantity
    else:
      self._items[product] = quantity
  
  def remove_item_full(self, product: Product):
    amount = self._items.get(product, 0)
    if amount:
      self._items.pop(product)
      store.add_product(product, amount)
    else:
      raise ValueError("Product not found in shopping cart")

  
  def remove_item_some(self, product: Product, to_remove: int):
    amount = self._items.get(product, 0)
    if not amount:
      raise ValueError("Product not found in shopping cart")
    
    if to_remove >= amount:
      self.remove_item_full(product)
    else:
      store.add_product(product, to_remove)
      self._items[product] = amount - to_remove
  
  def to_order(self):
    return Order(self._items)
  
  def clear(self):
    self._items = {}


class Customer:
  def __init__(self):
    self.orders = []
    self._shopping_cart = ShoppingCart()
    self.balance = 0.0

  def add_item_to_cart(self, product: Product):
    self._shopping_cart.add_item(product)
  
  def remove_item_from_cart(self, product: Product):
    self._shopping_cart.remove_item(product)
  
  def top_up(self, amount: float):
    self.balance += amount
  
  def checkout(self):
    order = self._shopping_cart.to_order()
    total = order.checkout()
    if self.balance < total:
      print("Not enough money! Top up or remove some items from your cart.")
    else:
      balance -= total
      orders += order
      self._shopping_cart.clear()