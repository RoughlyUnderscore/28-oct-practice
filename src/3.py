# This file would greatly benefit from the concept of Separation of Concerns,
# but that does not comply with the technical limitations of this task.
# lol

import os


TAX = float(os.getenv("TAX_PERCENTAGE") or "13") + 100 # convert to total


# Developer comment: moved "amount_available" away from Product
# into Store for a more adequate concern distribution.
class Product:
  """
  A class representing some arbitrary store product.

  Attributes:
    price (float): the base price of this product.
    category (str): the category of this product.
    sale (float): a sale, or lack thereof, imposed on this product (from 0.0 to 1.0).
  """

  def __init__(self, price: float, category: str, sale: float = 0.0):
    """
    Initialize a product.

    Parameters:
      price (float): the base price of this product.
      category (str): the category of this product.
      sale (float): a sale, or lack thereof, imposed on this product (from 0.0 to 1.0).
    """

    self.price = price
    self.category = category
    self.sale = sale
  
  def get_price(self):
    """
    Returns the current price of this product (including sale and tax).
    """

    return self.price * (1 - self.sale) * (TAX / 100)
  
  def set_sale(self, sale: float):
    """
    Imposes some sale on this product.

    Parameters:
      sale (float): the new sale for this product.
    """

    self.sale = sale
  
  def remove_sale(self):
    """
    Removes any ongoing sale from this product.
    """

    self.sale = 0.0


class Store:
  """
  A class representing a store with products in stock.

  Attributes:
    _products (dict[Product, int]): the current stock.
  """

  def __init__(self):
    """
    Initialize a store.
    """

    self._products: dict[Product, int] = {}
  
  def reserve_product(self, product: Product, amount: int):
    """
    Take some amount of some product away from the current stock
    (e.g. in order to put it away in a cart).

    Parameters:
      product (Product): the product in question.
      amount (int): how much to take.
    """

    total = self._products[product]
    if amount > total:
      raise ValueError("Not enough in stock")
    else:
      self._products[product] = total - amount
  
  def add_product(self, product: Product, amount: int = 1):
    """
    Add some amount of some product into the current stock.

    Parameters:
      product (Product): the product in question.
      amount (int): how much to add.
    """

    if product in self._products:
      self._products[product] += amount
    else:
      self._products[product] = amount


store = Store()
# initialize and add some products... idk i can't be bothered sorry


class Order:
  """
  Represents an order, either ongoing or finished.

  Attributes:
    items (dict[Product, int]): the ordered items.
  """

  def __init__(self, items: dict[Product, int]):
    """
    Initialize an order.

    Parameters:
      items (dict[Product, int]): the ordered items.
    """

    self.items = items
  
  def checkout(self) -> float:
    """
    Calculates the total price of this order.

    Returns:
      float: the total price.
    """

    return sum(
      amount * product.get_price() for (product, amount) in self.items.items()
      )


class ShoppingCart:
  """
  A class representing a shopping cart.
  
  Attributes:
    items (dict[Product, int]): the items in the cart.
  """

  def __init__(self):
    """
    Initialize a shopping cart.

    Attributes:
      items (dict[Product, int]): the items in the cart.
    """

    self._items: dict[Product, int] = {}
  
  def add_item(self, product: Product, quantity: int = 1):
    """
    Adds some amount of a product to the cart.

    Parameters:
      product (Product): the product in question.
      quantity (int): how much to add.
    """

    store.reserve_product(product, quantity)
    if product in self._items.keys():
      self._items[product] += quantity
    else:
      self._items[product] = quantity
  
  def remove_item_full(self, product: Product):
    """
    Removes a product from the cart.

    Parameters:
      product (Product): the product in question.
    """

    amount = self._items.get(product, 0)
    if amount:
      self._items.pop(product)
      store.add_product(product, amount)
    else:
      raise ValueError("Product not found in shopping cart")

  
  def remove_item_some(self, product: Product, to_remove: int):
    """
    Removes some amount of a product from the cart.

    Parameters:
      product (Product): the product in question.
      to_remove (int): how much to remove.
    """

    amount = self._items.get(product, 0)
    if not amount:
      raise ValueError("Product not found in shopping cart")
    
    if to_remove >= amount:
      self.remove_item_full(product)
    else:
      store.add_product(product, to_remove)
      self._items[product] = amount - to_remove
  
  def to_order(self):
    """
    Converts the current cart into a checkoutable order.

    Returns:
      Order: the newly made order.
    """

    return Order(self._items)
  
  def clear(self):
    """
    Clears out the cart.
    """

    self._items = {}


class Customer:
  """
  A class representing a customer.

  Attributes:
    orders (list[Order]): the customer's finished orders.
    _shopping_cart (ShoppingCart): the customer's current shopping cart.
    balance (float): the customer's balance.
  """

  def __init__(self):
    """
    Initialize a customer.
    """

    self.orders: list[Order] = []
    self._shopping_cart = ShoppingCart()
    self.balance = 0.0

  def add_item_to_cart(self, product: Product, quantity: int = 1):
    """
    Add a product to the cart.

    Parameters:
      product (Product): the product in question.
      quantity (int): how much to add.
    """
    
    self._shopping_cart.add_item(product, quantity)
  
  def remove_item_from_cart(self, product: Product, quantity: int = 1):
    """
    Removes a product from the cart.

    Parameters:
      product (Product): the product in question.
      quantity (int): how much to remove.
    """

    self._shopping_cart.remove_item_some(product, quantity)
  
  def top_up(self, amount: float):
    """
    Tops up the customer's balance.
    
    Parameters:
      amount (float): how much to top up.
    """

    self.balance += amount
  
  def checkout(self):
    """
    Purchases the customer's cart and adds it to their list of finished
    orders. Fails if the customer's balance is not enough to checkout.
    """
    
    order = self._shopping_cart.to_order()
    total = order.checkout()

    if self.balance < total:
      print("Not enough money! Top up or remove some items from your cart.")
    else:
      self.balance -= total
      self.orders.append(order)
      self._shopping_cart.clear()