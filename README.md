# VMAccess

**VMAccess** stands for **Virtual Machine Access**, a small client-server **RBAC utility for Hyper-V** _(Windows Server and Windows & Linux client machines supported)_.


## Getting Started

You'll need somewhat **20 minutes** to read this manual and configure your system.
Pay attention to [**Installation**](#installation) section especially.


### Prerequisites

**_If you're going to simply utilize this tool, you can skip straight to [**Installation**](README.md/#installation)._**


If you want to further develop VMAccess, you need to have installed:

- **Python 3.6** or newer _(though earlier versions of Python, starting from **Python 3.4**, will probably be fine, too)_;
- **`portalocker`** is used to guarantee that changes to log file would not be lost because of someone looking through log at the same time.
  Run **`python -m pip install portalocker`** in your terminal to install it;  look [here](https://pypi.python.org/pypi/portalocker) for more details.
- **`cx_Freeze`** is used to build the executables out of source files; more details [here](https://anthony-tuininga.github.io/cx_Freeze/).

Additionally, we recommend to use either _PyCharm_ ([_Community Edition_](https://anthony-tuininga.github.io/cx_Freeze/) is fine) or [_VSCode_](https://code.visualstudio.com/Download) for development.


### Installation

#### 1. Getting binaries

There are two general ways to get binaries of VMAccess:

1. Copy **`\bin\VMAccess_client`** and **`\bin\VMAccess_server`** folders to your client machines and to the server respectively.

2. Compile the binaries from source `.py` files yourself, running **`setup_client.py`** and **`setup_server.py`**:  
  
  ```
  #Assuming you've open your terminal/command line in VMAccess directory:

  python setup_client.py build
  python setup_server.py build
  ```

  The resulting folders **`bin\VMAccess_client-YY.MM.DD.-HH.MM.SS`** and **`bin\VMAccess_server-YY.MM.DD.-HH.MM.SS`** should be copied to the client machines and to the server respectively.  
  
  To change default folders for binaries you should replace the  
  **`"build_exe": "bin/VMAccess...`**  
  strings in **`setup_client.py`** and **`setup_server.py`** with the commented strings with your own values:  
  
  ```
  #From 'setup_client.py':

  build_exe_options = {
      "build_exe": "I_can_pick_whatever_name_and_path_I_want",    #just because I can! Pickle Rick!
      ...
  }
  ``` 

#### 2. Configuration files

Now you have **2 files that need to be configured**: **`VMAccess_client.cfg`** in your 'client' folder and **`VMAccess_server.cfg`** in your 'server' folder.

Change them in a way that fits your purposes:

**In `VMAccess_client.cfg`:**
  - `host = <IP>` - replace `<IP>` to your server ip address;
  - `port = <PORT>`- replace `<PORT>` with your server's port;
  - `token = <TOKEN>` - replace `<TOKEN>` with whatever unique user identificator (it must not have spaces). This is used for authentification.


**In `VMAccess_server.cfg`:**
  - `log = "log.log"` - replace `log.log` with the path to the file you want to use as log. If it does not exist, it will be created. _Note that filenames are framed with `""`._
  - `host = <IP>` - replace `<IP>` to the **ip address you want to allow connections from**; leave `0.0.0.0` in case you want to allow all ip addresses;
  - `port = <PORT>`- replace `<PORT>` with your server's port;
  - `keyfile = "key.key"` and `certfile = "cert.cert"` - replace `key.key` and `cert.cert` with paths to your SSL certificates. _Note that filenames are framed with `""`._

**IMPORTANT:** in `VMAccess_server.cfg`, below the `#Clients` string, place information about each client (identified with unique token) with the following syntax:

```
#Clients:

#345678                #Client's token; '#' SIGN IN FRONT OF TOKEN IS OBLIGATORY!
$ClusterName = HVCL    #CLuster name which will be used in Powershell filtered search
$VMFilter = test       #Name that will be used as a filter to search for VMs

...

```


#### 3. Setting up server application as Windows Service (OPTIONAL)

If you want server application to autostart, you should make it a Windows Service.

To achieve that, we highly recommend using [NSSM](https://nssm.cc/). Download it [here](https://nssm.cc/download).

To set up the service properly, follow [this instruction](https://nssm.cc/usage).


## 3. VMAccess user interface

VMAccess user interface is a regular console interface. 

If client's token was correct, user is provided with a list of all VMs that are available for them to manage.

To choose a particular machine they need to type a valid index of VM from the list.

User can **`start`**, **`stop`**, **`restart`** and **`shutdown`** chosen VM or get back to the list of all VMs available by typing **`return`**. 

Information about exact VM can be manually updated with **`status`** command and is updated automatically after any command is sent.

List of VMs can be manually refreshed with **`refresh`** command and is updated automatically after any command is sent.

You can always get a list of available commands by typing **`help`**.

The program can be exited either by typing **`exit`** command or pressing **`Ctrl` + `C`**.



## Authors

* **Anton Potapov** - *Powershell commands, system design & debugging* - [workservice](https://github.com/workservice)
* **Roman Krivonogov** - *Python implementation & docs* - [FourthRome](https://github.com/FourthRome) 



## License

This project is licensed under the  GNU GPLv3 - see the [LICENSE.md](LICENSE.md) file for details.