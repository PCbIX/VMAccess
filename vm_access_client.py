import socket
import os
import ssl
import threading
import sys

def prompt():
    print('<VMACCESS>', end='')

def u_recv(sock, maxsize):
    return sock.recv(maxsize).decode('utf-8')

def u_send(sock, message):
    sock.send(message.encode('utf-8'))

def main(argv=None):
    if argv is None:
        argv = sys.argv

    title = 'VMAccessClient v0.1'
    os.system("title " + title)

    host = None
    port = None
    token = None

    with open('client.cfg', 'r') as cfg: 
        for line in cfg:
            if line.startswith('host'):
                host = line.split()[2]
            elif line.startswith('port'):
                port = int(line.split()[2])
            elif line.startswith('token'):
                token = line.split()[2]
            if host is not None and port is not None and token is not None:
                break

    if host is None:
        print('Error occurred: information about host is not found!')
        return 1
    elif port is None:
        print('Error occurred: information about port is not found!')
        return 1
    elif token is None:
        print('Error occurred: information about token is not found!')
        return 1

    raw_s = None
    s = None

    try:
        raw_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as e:
        print('Error occurred: failed to set up socket!\r\n%s' %(e))
        return 1

    try:
        s = ssl.wrap_socket(
          raw_s,
          ssl_version=ssl.PROTOCOL_TLSv1_2,
          ciphers='AES256-SHA256')
    except SSLError as e:
        print('Error occurred: failed to set up SSL!\r\n%s' %(e))
        return 1

    try:
        s.connect((host, port))
    except OSError as e:
        print('Error occurred: failed to connect to server!\r\n%s' %(e))
        return 1

    try:
        max_msg_size = 4096
        
        u_send(s, token)
        data = u_recv(s, max_msg_size)

        if data:
            os.system('cls')
            print(data)
            prompt()

            vm_chosen = False
            command = input()
            
            while (command):
                if vm_chosen:
                    if (command == 'exit'):
                        os.system('cls')
                        s.close()
                        return 0
                    elif (command == 'help'):
                        os.system('cls')
                        print('HERE ARE THE COMMANDS YOU CAN USE NOW:\r\n\r\n'
                          'restart ------- Restart current VM\r\n'
                          'stop ---------- Stop current VM\r\n'
                          'start --------- Start current VM\r\n'
                          'shutdown ------ Shutdown current VM '
                          '(send signal to OS)\r\n' 
                          'status -------- Get info about current VM\r\n'
                          'return -------- Get back to the list of VMs\r\n'
                          'exit ---------- Get the hell out of all '
                          'this VM stuff\r\n'
                          'help ---------- Guess what? NOT VM\r\n')
                        prompt()
                    else:
                        if (command == 'return'):
                            vm_chosen = False
                        u_send(s, command)
                        data = u_recv(s, max_msg_size)
                        os.system('cls')
                        print(data)
                        prompt()
                else:
                    if (command == 'exit'):
                        os.system('cls')
                        s.close()
                        return 0
                    elif (command == 'help'):
                        os.system('cls')
                        print('YOU CAN TYPE THE NUMBER OF VM YOU WANT TO '
                          'MANAGE OR ONE OF THE FOLLOWING COMMANDS:\r\n\r\n'
                          'refresh ------- Refresh the list of VMs\r\n'
                          'exit ---------- Exit\r\n'
                          'help ---------- Help page\r\n')
                        prompt()
                    else:
                        u_send(s, command)
                        data = u_recv(s, max_msg_size)
                        os.system('cls')
                        print(data)
                        prompt()
                        if not data.startswith('Sorry'):
                            vm_chosen = True

                command = input()

    except KeyboardInterrupt:
        print('Keyboard interrupt detected, stopping the client...\n%s' %(e))
    finally:
        s.close()
        os.system('cls')
        return 1


if __name__ == "__main__":
    sys.exit(main())
