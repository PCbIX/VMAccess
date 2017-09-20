import sys
import time
from cx_Freeze import setup, Executable

build_exe_options = {
  "build_exe": "../BUILDs/build_server%s" %(time.strftime(" - %y.%m.%d-%H.%M.%S")),
  "packages": [
    "select",
    "socket",
    "time",
    "ssl",
    "sys",
    "portalocker",
    "vm_access_terminal",
    "vm_access_parse",
    "os"
  ],
  "excludes": [],
  "zip_include_packages": "*",
  "zip_exclude_packages": []
}

base = None
#if sys.platform == "win32":
#    base = "Win32GUI"

setup(
    name = "VMAccessServer",
    version = "0.1",
    description = "VMAccessServer",
    options = {"build_exe": build_exe_options},
    executables = [Executable("vm_access_server.py", base=base)]
)