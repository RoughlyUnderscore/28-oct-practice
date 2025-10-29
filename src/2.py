from abc import ABC, abstractmethod

class Vehicle(ABC):
  """
  An abstract class representing some vehicle.
  """

  @abstractmethod
  def _info(self) -> str:
    """
    A method for describing this vehicle.

    Returns:
      str: the description of the vehicle.
    """

    pass

  def __str__(self):
    return self._info()


class Car(Vehicle):
  """
  A class representing a car. Inherits from Vehicle.
  """

  def _info(self):
    return "I am a car! I can zoom across the highway blazingly fast."


class Bus(Vehicle):
  """
  A class representing a bus. Inherits from Vehicle.
  """

  def _info(self):
    return "I am a bus! I hold many passengers but sometimes it gets really claustrophobic here."


class Train(Vehicle):
  """
  A class representing a train. Inherits from Vehicle.
  """

  def _info(self):
    return "I am a train and I am the most ecologically clean means of transport!"


car = Car()
bus = Bus()
train = Train()

print(car)
print(bus)
print(train)

# or:
print(car._info())
print(bus._info())
print(train._info())