from sys import argv
import os
import subprocess
import sys
import pip
from pip._internal import main as pipmain

def install(package):
    # pipmain(["install", "--upgrade", "--force-reinstall", package])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "--force-reinstall", package], shell=True)

args = argv[1:]

def run():
    print(f"I just ran, with {args = }!")

def save():
    print(f"You just hot saved, with {args = }!")

def upgrade():
    install("git+https://github.com/FredslundMagnus/python-helpers.git")
    # print("C:/Users/magnu/AppData/Local/Microsoft/WindowsApps/python.exe -m pip install --upgrade --force-reinstall git+https://github.com/FredslundMagnus/python-helpers.git")