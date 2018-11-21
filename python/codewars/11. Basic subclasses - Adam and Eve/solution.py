class Human:
 pass
class Man(Human):
 pass
class Woman(Human):
 pass
def God():
 Adam = Man()
 Eva = Woman()
 return [Adam,Eva]
 
paradise = God()
test.assert_equals(isinstance(paradise[0], Man) , True, "First object are a man")