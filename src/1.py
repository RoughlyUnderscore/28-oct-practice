import math
from enum import Enum
from abc import ABC, abstractmethod


class Employee(ABC):
  """
  A class representing an arbitrary employee.

  Attributes:
    salary (float): Employee's base salary.
    work_hrs (int): Employee's daily work hour amount.
    months_worked (int): Employee's current amount of months worked at the company.
    coef (float): Employee's salary calculation coefficient.
  """

  def __init__(self, salary: float, work_hrs: int, months_worked: int, coef: float):
    """
    Initialize an employee.

    Parameters:
      salary (float): Employee's base salary.
      work_hrs (int): Employee's daily work hour amount.
      months_worked (int): Employee's current amount of months worked at the company.
      coef (float): Employee's salary calculation coefficient.
    """
    self.salary = salary
    self.work_hrs = work_hrs
    self.months_worked = months_worked
    self.coef = coef
  

  @abstractmethod
  def calculate_salary(self) -> float:
    """
    Calculate an employee's salary according to some algorithm.

    Returns:
      float: the total salary.
    """
    ...


class DeveloperLevel(Enum):
  """
  An enum representing developer levels' salary coefficients.
  """

  JUNIOR = 1.0
  MIDDLE = 1.2
  SENIOR = 1.4


class Manager(Employee):
  """
  A class representing a manager. Inherits from Employee.

  Attributes:
    salary (float): Employee's base salary.
    work_hrs (int): Employee's daily work hour amount.
    months_worked (int): Employee's current amount of months worked at the company.
    coef (float): Employee's salary calculation coefficient.
    _growth_rate (int): Internal value for calculating how fast the salary grows proportionally to months_worked.
    ceiling (float): The maximum salary of this employee.
  """

  def __init__(self):
    """
    Initialize a manager.
    """

    super().__init__(90_000, 9, 0, 1.15)
    self._growth_rate = 24
    self.ceiling = 150000.0
  
  def _complementary(self):
    """
    Calculate the complementary value such that the calculation for month 1
    results in just the base salary.
    """

    return self._growth_rate ** (1/self.coef)
  
  def calculate_salary(self):
    return min(
      self.salary * self.coef * (
        math.log(self.months_worked + self._complementary(), self._growth_rate)
        ),
      self.ceiling
    )


class Developer(Employee):
  """
  A class representing a developer. Inherits from Employee.

  Attributes:
    salary (float): Employee's base salary.
    work_hrs (int): Employee's daily work hour amount.
    months_worked (int): Employee's current amount of months worked at the company.
    coef (float): Employee's salary calculation coefficient.
    level (DeveloperLevel): The current skill level of this developer.
    _growth_rate (int): Internal value for calculating how fast the salary grows proportionally to months_worked.
  """

  def __init__(self):
    """
    Initialize a developer.
    """

    super().__init__(110_000, 10, 0, 1.25)
    self.level = DeveloperLevel.JUNIOR
    self._growth_rate = 18
  
  def _coef(self):
    """
    Calculate the total salary coefficient of this developer.
    """
    
    return self.coef * self.level.value
  
  def _complementary(self):
    """
    Calculate the complementary value such that the calculation for month 1
    results in just the base salary.
    """

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