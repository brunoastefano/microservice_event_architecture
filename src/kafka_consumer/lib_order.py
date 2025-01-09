import json
import pytz
from datetime import datetime
from types import SimpleNamespace

class CreatedOrder():
  def __init__(self, orderId: int, customerId: int, items, total: float):
    self.orderId = orderId
    self.customerId = customerId
    self.items = items
    self.total = total

class ProcessedOrder():
  def __init__(self, orderId: int, status, processedAt, discountApplied: float):
    self.orderId = orderId
    self.status = status
    self.processedAt = processedAt
    self.discountApplied = discountApplied

class Order():
  def __init__(self, customerId: int, items, total: float):
    self.orderId = None
    self.customerId = customerId
    self.status = 0
    self.items = items
    self.originalValue = total
    self.discountApplied = 0.0
    self.total = total
    self.processedAt = datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%Z")

  @classmethod
  def initFromCreatedOrderJSON(cls, createdOrderMsg):
    orderDict = json.loads(createdOrderMsg)
    orderId = orderDict["orderId"]
    customerId = orderDict["customerId"]
    items = orderDict["items"]
    total = orderDict["total"]
    order = cls(customerId, items, total)
    order.setId(orderId)
    return order
  
  def setId(self, orderId: int):
    if self.orderId is None:
      self.orderId = orderId
    else:
      raise Exception("Order already has Id")
  
  def setDiscount(self, discount: float):
    self.discountApplied = discount
    self.total = self.originalValue - self.discountApplied
    self.status = 1
    self.processedAt = datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%Z")
  
  def toJSON(self):
    order = self
    if self.status == 0:
      order = CreatedOrder(orderId = self.orderId,
                          customerId = self.customerId,
                          items = self.items,
                          total = self.total)
    elif self.status == 1:
      order = ProcessedOrder(orderId = self.orderId,
                            status = "processed",
                            processedAt = self.processedAt,
                            discountApplied = self.discountApplied)

    return json.dumps(
        order,
        default=lambda o: o.__dict__,
        sort_keys=False,
        indent=4)
