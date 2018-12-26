import socket
import os
import ssl
import sys

from console_formatting import prompt, print_error

max_msg_size = 4096
VERSION = "v1.1"
TITLE = "VMAccessClient " + VERSION

def u_recv(sock, maxsize):
    return sock.recv(maxsize).decode('utf-8')

def u_send(sock, message):
    sock.send(message.encode('utf-8'))

def main():
    os.system("title " + TITLE)

    host = None
    port = None
    token = None

    with open('VMAccess_client.cfg', 'r') as cfg: 
        for line in cfg:
            if line.startswith('host'):
                host = line.split("=")[1].strip().split()[0]
            elif line.startswith('port'):
                port = int(line.split("=")[1].strip().split()[0])
            elif line.startswith('token'):
                token = line.split("=")[1].strip().split()[0]
            if host and port and token is not None:
                break
    

    if not host:
        print_error("host is not specified")
        return 1
    elif not port:
        print_error("port is not specified")
        return 1
    elif token is None:
        print_error("token is not specified")
        return 1

    try:
        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as e:
        print_error("failed to set up socket", e)
        return 1

    try:
        sock = ssl.wrap_socket(
                raw_sock,
                ssl_version=ssl.PROTOCOL_TLSv1_2,
                ciphers='AES256-SHA256')
    except SSLError as e:
        print_error("failed to set up SSL!", e)
        return 1

    try:
        sock.connect((host, port))
    except OSError as e:
        print_error("failed to connect to server!", e)
        return 1

    try:
        u_send(sock, token)
        data = u_recv(sock, max_msg_size)

        if data:
            prompt(data)
            vm_chosen = False
            command = input()
            
            while (command != "exit"):
                if not command:
                    prompt("", clear=False)
                elif vm_chosen:
                    if (command == "help"):
                        prompt("HERE ARE THE COMMANDS YOU CAN USE NOW:\n\n"
                               "restart ------- Restart current VM\n"
                               "stop ---------- Stop current VM\n"
                               "start --------- Start current VM\n"
                               "shutdown ------ Shutdown current VM (send signal to OS)\n"
                               "status -------- Get info about current VM\n"
                               "return -------- Get back to the list of VMs\n"
                               "exit ---------- Get the hell out of all this VM stuff\n"
                               "help ---------- Guess what? NOT VM\n")
                    else:
                        if (command == "return"):
                            vm_chosen = False
                        u_send(sock, command)
                        prompt(u_recv(sock, max_msg_size))
                else:
                    if (command == "help"):
                        prompt("YOU CAN TYPE THE NUMBER OF VM YOU WANT TO MANAGE OR ONE OF THE FOLLOWING COMMANDS:\n\n"
                               "refresh ------- Refresh the list of VMs\n"
                               "exit ---------- Exit\n"
                               "help ---------- Help page\n")
                    else:
                        u_send(sock, command)
                        data = u_recv(sock, max_msg_size)
                        prompt(data)

                        if not data.startswith("Sorry"):
                            vm_chosen = True

                command = input()

    except KeyboardInterrupt:
        print("Keyboard interrupt detected, stopping the client...\n{0}".format(e))
    finally:
        sock.close()
        os.system('cls')
        return 0


if __name__ == "__main__":
    sys.exit(main())
