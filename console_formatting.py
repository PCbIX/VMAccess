import os

ERROR_TAG = "ERROR: "

def prompt(text, clear=True):
    if clear:
        os.system('cls')
    print(text, "<VMACCESS>", end="", sep= "\n" if text else "")

def print_error(text="", err=None):
    print("{0}{1}{2}{3}".format(ERROR_TAG, text, "\n" if err else "", err or ""))