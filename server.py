from main import Defaults
from inspect import signature

print("SERVER")
print(signature(Defaults.generate))

Defaults.generate(b=4, a=3, d=3)

print(signature(Defaults.__init__))
