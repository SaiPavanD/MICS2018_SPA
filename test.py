def example():
    print "Hello"
    example2()

def example2():
    print "Hello2"

class Blah:
    def displayCount(self):
        print "qwerty"

class Employee(Blah):
   'Common base class for all employees'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1

   def displayCount(self):
     print "Total Employee %d" % Employee.empCount
     example()

   def displayEmployee(self):
      print "Name : ", self.name,  ", Salary: ", self.salary



emp1 = Employee("ABC", 2000)

emp1.displayCount()

a = example()
