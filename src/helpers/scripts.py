from sys import argv
import os
args = argv[1:]

def run():
    print(f"I just ran, with {args = }!")

def save():
    print(f"You just hot saved, with {args = }!")

def upgrade():
    print("C:/Users/magnu/AppData/Local/Microsoft/WindowsApps/python.exe -m pip install --upgrade --force-reinstall git+https://github.com/FredslundMagnus/python-helpers.git")