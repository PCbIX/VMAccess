import select
import socket
import time
import sys
import ssl
import os

import portalocker

import vm_access_terminal as vmat
import vm_access_parse as vmap


class Logger(object):
    def __init__(self):
        self.console = sys.stdout
        log_file = ''
        with open('config.cfg', 'r') as cfg:
            for line in cfg:
                if line.startswith('log'):
                    log_file = line.split('"')[1]
        try:
            self.log = open(log_file, "a")
            portalocker.lock(self.log, portalocker.LOCK_EX)
        except (IOError, LockException) as e :
            print('Cannot lock log file: %s raised\r\n%s' %(e))
            self.log.close()
            sys.exit()
        self.log.write('###############################################'
          '#######################\n%sServer started\n'
          %time.strftime("%y.%m.%d/%H:%M:%S - "))

    def flush(self):
        self.log.flush()
        self.console.flush()

    def write(self, message):
        self.console.write(message)
        self.log.write(message)
        self.flush()

    def __exit__(self, exception_type, exception_value, traceback):
        self.log.close()
        self.console.close()


class PowershellSession:
    def __init__(self, sock):
        self._sock = sock
        self._term = None
        self._auth = False
        self._chosen_vm = ''
        self._token = None
        
    def token(self):
        return self._token
        
    def socket(self):
        return self._sock

    def status(self):
        return self._auth

    def authentificate(self, data):
        cfg = vmap.read_cfg(data)
        if cfg is not None:
            self._term = vmat.Terminal(cfg)
            self._auth = True
            self._token = cfg[0]
            return self._term.get_vm_list()
        else:
            return None

    def manage(self, data):
        if self._chosen_vm:
            if data == 'restart':
                self._term.manage_vm('Restart-VM')
                print('%sToken #%s restarted %s'
                  %(time.strftime("%y.%m.%d/%H:%M:%S - "),
                  self._token, self._chosen_vm))
                return self._term.vm_status()
            elif data == 'stop':
                self._term.manage_vm('Stop-VM -TurnOff')
                print('%sToken #%s stopped %s'
                  %(time.strftime("%y.%m.%d/%H:%M:%S - "),
                  self._token, self._chosen_vm))
                return self._term.vm_status()
            elif data == 'shutdown':
                self._term.manage_vm('Stop-VM')
                print('%sToken #%s shutdowned %s'
                  %(time.strftime("%y.%m.%d/%H:%M:%S - "),
                  self._token, self._chosen_vm))
                return self._term.vm_status()
            elif data == 'start':
                self._term.manage_vm('Start-VM')
                print('%sToken #%s started %s'
                  %(time.strftime("%y.%m.%d/%H:%M:%S - "),
                self._token, self._chosen_vm))
                return self._term.vm_status()
            elif data == 'status':
                return self._term.vm_status()
            elif data == 'return':
                self._chosen_vm = self._term.choose_vm(0)
                return self._term.get_vm_list()
            else:
                return ("Sorry, seems like you've mistyped!\n\n%s"
                  %(self._term.vm_status()))
        else:
            if data == 'refresh':
                return self._term.get_vm_list()
            else:
                try:
                    num = int(data)
                    reply = self._term.choose_vm(num)
                    if reply:
                        self._chosen_vm = reply
                        return self._term.vm_status()
                    else:
                        return ("Sorry, there's no VM with such number! "
                          "Try something else.\n\n%s"
                          %(self._term.get_vm_list()))
                except ValueError:
                    return ("Sorry, seems like you've mistyped!\n\n%s"
                      %(self._term.get_vm_list()))
    
    def close(self):
        if self._term is not None:
            self._term.close()
        self._sock.close()


class PowershellSessionPool:
    def __init__(self):
        self._list = []

    def append(self, sock):
        self._list.append(PowershellSession(sock))

    def find_session(self, sock):
        for session in self._list:
            if (session.socket()) == sock:
                return session
        return None

    def remove(self, sock):
        session = self.find_session(sock)
        if session is not None:
            session.close()
            self._list.remove(session)


def u_recv(sock, maxsize):
    return sock.recv(maxsize).decode('utf-8')

def u_send(sock, message):
    sock.send(message.encode('utf-8'))


def main(argv=None):
    if argv is None:
        argv = sys.argv

    title = 'VMAccessServer v0.1.1'
    os.system("title " + title)

    sys.stdout = Logger()

    host = None
    port = None
    keyfile = None
    certfile = None

    with open('config.cfg', 'r') as cfg: 
        for line in cfg:
            if line.startswith('host'):
                host = line.split()[2]
            elif line.startswith('port'):
                port = int(line.split()[2])
            elif line.startswith('keyfile'):
                keyfile = line.split('"')[1]
            elif line.startswith('certfile'):
                certfile = line.split('"')[1]
            if (host is not None and port is not None
              and keyfile is not None and certfile is not None):
                break

    if host is None:
        print('Error occurred: information about host is not found!')
        return 1
    elif port is None:
        print('Error occurred: information about port is not found!')
        return 1
    elif keyfile is None:
        print('Error occurred: information about SSL key is not found!')
        return 1
    elif certfile is None:
        print('Error occurred: information about SSL certfile is not found!')
        return 1

    raw_server = None
    server = None

    try:
        raw_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError as e:
        print('Error occurred: failed to set up socket!\r\n%s' %(e))
        return 1

    try:
        server = ssl.wrap_socket(
          raw_server,
          keyfile=keyfile,
          certfile=certfile,
          server_side=True,
          ssl_version=ssl.PROTOCOL_TLSv1_2,
          ciphers='AES256-SHA256')
    except SSLError as e:
        print('Error occurred: failed to set up SSL!\r\n%s' %(e))
        return 1

    simultaneous_sessions = 10
    max_msg_size = 4096

    try:
        server.bind((host,port))
        server.listen(simultaneous_sessions)
    except OSError as e:
        print('Error occurred: failed to set up listening port!\r\n%s' %(e))
        return 1

    input = [server,]
    pool = PowershellSessionPool()
    running = True
    
    try:
        while running:
            try:
                inputready, outputready, exceptready =\
                  select.select(input, [], [], 1)
            except OSError:
                print('Error occurred: select from active sockets crushed!'
                  '\r\n%s' %(e))
                for sock in input:
                    close(sock)
                return 1
        
            for s in inputready:
                if s == server:
                    client, address = server.accept()
                    input.append(client)
                    pool.append(client)
                    print ('%sNew client added%s'
                      %(time.strftime("%y.%m.%d/%H:%M:%S - "), str(address)))
                else:
                    session = pool.find_session(s)
                    data = u_recv(s, max_msg_size)
                    if data:
                        if session.status():
                            answer = session.manage(data)
                            u_send(s, answer)
                        else:
                            answer = session.authentificate(data)
                            if answer is not None:
                                print ('%sAuthentification successful for '
                                  'token #%s'
                                  %(time.strftime("%y.%m.%d/%H:%M:%S - "),
                                  str(data)))
                                u_send(s, answer)
                            else:
                                print ('%sAuthentification failed for token '
                                  '#%s'
                                  %(time.strftime("%y.%m.%d/%H:%M:%S - "),
                                  str(data)))
                                pool.remove(s)
                                input.remove(s)
                    else:
                        print ('%sToken #%s disconnected'
                          %(time.strftime("%y.%m.%d/%H:%M:%S - "),
                          session.token()))
                        pool.remove(s)
                        input.remove(s)
                        
    except KeyboardInterrupt as e:
        print('Keyboard interrupt detected, stopping the server...\n%s' %(e))
    finally:
        for s in input:
            s.close()
        return 0


if __name__ == "__main__":
    sys.exit(main())
