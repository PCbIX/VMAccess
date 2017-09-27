import time
from cx_Freeze import setup, Executable

build_exe_options = {
  "build_exe": "bin/VMAccess_client%s" %(time.strftime("-%y.%m.%d-%H.%M.%S")),
  #"build_exe": "bin/VMAccess_client",
  "packages": ["os", "ssl", "sys"],
  "excludes": [],
  "zip_include_packages": "*",
  "zip_exclude_packages": []
}

base = None

setup(
    name = "VMAccessClient",
    version = "0.1.1",
    description = "VMAccessClient",
    options = {"build_exe": build_exe_options},
    executables = [Executable("vm_access_client.py", base=base)]
)