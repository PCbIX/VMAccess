import sys
import time
from cx_Freeze import setup, Executable

build_exe_options = {
  "build_exe": "../BUILDs/build_client%s" %(time.strftime(" - %y.%m.%d-%H.%M.%S")),
  "packages": ["os", "ssl", "sys"],
  "excludes": [],
  "zip_include_packages": "*",
  "zip_exclude_packages": []
}

base = None
#if sys.platform == "win32":
#    base = "Win32GUI"

setup(
    name = "VMAccessClient",
    version = "0.1",
    description = "VMAccessClient",
    options = {"build_exe": build_exe_options},
    executables = [Executable("vm_access_client.py", base=base)]
)