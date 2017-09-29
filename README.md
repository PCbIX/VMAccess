# VMAccess

**VMAccess** stands for **Virtual Machine Access**, a small client-server **RBAC utility for Hyper-V** (Windows Server and Windows & Linux client machines supported).


## Getting Started

VMAccess is extremely easy to use, but you'll need somewhat 30 minutes to fully understand the requirements for the most reliable system configuration.
Don't worry, there's nothing sophisticated about it; you just need to read this manual carefully, [**Prerequisites**](#prerequisites) and [**Installation**](#installation) sections especially.


### Prerequisites

_If you're going to simply utilize this tool, you can skip straight to [**Installing**](README.md/#installation)._

To launch client and server applications there are no special requirements - all files are already included.

If you want to further develop VMAccess, you need to have installed:

- **Python 3.6** or newer _(though earlier versions of Python, starting from **Python 3.4**, will probably be fine, too)_;
- `portalocker` is used to guarantee that changes to log file would not be missed because of someone looking through log at the same time.
  Run `python -m pip install portalocker` in your terminal to install it;  look [(here)](https://pypi.python.org/pypi/portalocker) for more details on `portalocker`;
- `cx_Freeze` is used to build the executables out of source files; more details on `cx_Freeze` [here](https://anthony-tuininga.github.io/cx_Freeze/).

Additionally, we recommend to use either _PyCharm_ ([_Community Edition_](https://anthony-tuininga.github.io/cx_Freeze/) is fine) or [_VSCode_](https://code.visualstudio.com/Download) for development, though this advice is one big IMHO and is ridiculous in case you already have a Python IDE you're comfortable with.


### Installation

#### 1. Getting binaries

There are two general ways to get binaries of VMAccess:
  1. Copy `\bin\VMAccess_client` and `\bin\VMAccess_server` folders to your client machines and to the server respectively. You can place them anywhere or even extract their contents, but please keep `.exe` files in the same folder with `library.rar`.
  
  2. Compile the binaries from source `.py` files yourself, runnning `setup_client.py` and `setup_server.py`:

  ```
  #Assuming you've open your terminal/command line in VMAccess directory:

  python setup_client.py build
  python setup_server.py build
  ```

  The resulting folders `VMAccess_client-YY.MM.DD.-HH.MM.SS` and `VMAccess_server-YY.MM.DD.-HH.MM.SS` should be copied to the client machines and to the server respectively (just like mentioned above in paragraph 1).
  
  You may reasonably like to see more convenient names of resulting folders, so to change them you can either replace the `"build_exe": "bin/VMAccess...` strings in `setup_client.py` and `setup_server.py` with the commented strings (you'll get `\bin\VMAccess_client` and `\bin\VMAccess_server` folders this way) or even with your own values:

  **From `setup_client.py`:**
  ```
  build_exe_options = {
      #"build_exe": "bin/VMAccess_client%s" %(time.strftime("-%y.%m.%d-%H.%M.%S")), #This name is lame! No way!
      "build_exe": "I_can_pick_whatever_name_and_path_I_want", #just because I can! Pickle Rick!
      "packages": ["os", "ssl", "sys"],
      "excludes": [],
      "zip_include_packages": "*",
      "zip_exclude_packages": []
  }
  ``` 


#### 2. Configuration files

Now you have **2 files that need to be configured**: `VMAccess_client.cfg` in your 'client' folder and `VMAccess_server.cfg` in your 'server' folder.

Change them in a way that fits your purposes:

**In `VMAccess_client.cfg`:**
  - `host = <IP>` - replace `<IP>` to your server ip address;
  - `port = <PORT>`- replace `<PORT>` with your server's port;
  - `token = <TOKEN>` - replace `<TOKEN>` with whatever unique user identificator; this is used for authentification.

**In `VMAccess_server.cfg`:**
  - `log = "log.log"` - replace `<LOG>` with the path to the file you want to use as log; if it does not exist, it will be created;  
  - `host = <IP>` - replace `<IP>` to the **ip address you want to allow connections from**; leave `0.0.0.0` in case you want to allow all ip addresses;
  - `port = <PORT>`- replace `<PORT>` with your server's port;
  - `keyfile = "key.key"` and `certfile = "cert.cert"` - replace `key.key` and `cert.cert` with paths to your SSL certificates; note that filenames are framed with `""`

**IMPORTANT:** in `VMAccess_server.cfg`, below the `#Clients` string, place information about each client (identified with unique token) with the following syntax:

```

#345678 #Client's token
$ClusterName = HVCL #CLuster name which will be used in Powershell filtered search
$VMFilter = test #Name that will be used as a filter to search for VMs

```

#### 3. Setting up server application as Windows Service (OPTIONAL)

You can, for sure, just launch your server application every time you start the server, but there's a more automated way - to make our server application a Windows Service.

To achieve that, we highly recommend using [NSSM](https://nssm.cc/). Download it [here](https://nssm.cc/download).

To set up the service properly, follow [this instruction](https://nssm.cc/usage).

#### 4. YOU'RE AWESOME!

## 3. Using VMAccess


## Authors

* **Anton Potapov** - *Powershell commands, system design & debugging* - [workservice](https://github.com/workservice)
* **Roman Krivonogov** - *Python implementation & docs* - [FourthRome](https://github.com/FourthRome) 

## License

This project is licensed under the  GNU GPLv3 - see the [LICENSE.md](LICENSE.md) file for details.