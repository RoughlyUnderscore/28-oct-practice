import math
from enum import Enum
from abc import ABC, abstractmethod


class Employee(ABC):
  def __init__(self, salary, work_hrs, months_worked, coef):
    self.salary = salary
    self.work_hrs = work_hrs
    self.months_worked = months_worked
    self.coef = coef
  

  @abstractmethod
  def calculate_salary(self) -> int:
    ...


class DeveloperLevel(Enum):
  JUNIOR = 1.0
  MIDDLE = 1.2
  SENIOR = 1.4


class Manager(Employee):
  def __init__(self):
    super().__init__(90_000, 9, 0, 1.15)
    self._growth_rate = 24
    self.ceiling = 150000
  
  def _complementary(self):
    return self._growth_rate ** (1/self.coef)
  
  def calculate_salary(self):
    return min(
      self.salary * self.coef * (
        math.log(self.months_worked + self._complementary(), self._growth_rate)
        ),
      self.ceiling
    )


class Developer(Employee):
  def __init__(self):
    super().__init__(110_000, 10, 0, 1.25)
    self.level = DeveloperLevel.JUNIOR
    self._growth_rate = 18
  
  def _coef(self):
    return self.coef * self.level.value
  
  def _complementary(self):
    return self._growth_rate ** (1 / self._coef())
  
  def calculate_salary(self):
    return self.salary * self.coef * (
      math.log(self.months_worked + self._complementary(), self._growth_rate)
      )
  

manager = Manager()
for i in range(121):
  print(f"Months worked: {manager.months_worked} | Salary: {manager.calculate_salary()}")
  manager.months_worked += 1

print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")

developer = Developer()
for i in range(121):
  print(f"Months worked: {developer.months_worked} | Salary: {developer.calculate_salary()}")
  developer.months_worked += 1