import subprocess as sp

import vm_access_parse as vmap


class Terminal:
    def __init__(self, cfg):
        self._proc = sp.Popen(
          ['powershell'], stdin=sp.PIPE, stdout=sp.PIPE,
          stderr=sp.STDOUT, encoding='cp866')
        self._token = cfg[0]
        self._cluster_name = cfg[1]
        self._vm_filter = cfg[2]
        self._vm_list = []
        self.clear()
        
    def flush(self):
        self._proc.stdin.flush()
        self._proc.stdout.flush()

    def write(self, command, finish=True):
        self._proc.stdin.write('%s\n' %(command))
        if finish:
            self._proc.stdin.write("''\n")
        self.flush()

    def read(self):
        res = []
        line = self._proc.stdout.readline()
        while not line.endswith("''\n"):
            if not line.startswith('\n') and not line.startswith('\r\n'):
                res.append(line)
            line = self._proc.stdout.readline()
        return res

    def clear(self):
        self._proc.stdin.write('""\n')
        self.flush()
        line = self._proc.stdout.readline()
        while not line.endswith('""\n'):
            line = self._proc.stdout.readline()

    def get_vm_list(self):
        self.write('$CR = Get-Cluster "*%s*" | Get-ClusterResource | '
          '? ResourceType -EQ "Virtual Machine"' %(self._cluster_name))
        self.write('$FVM = $CR | ? Name -Like "*%s*" | '
          'Get-VM' %(self._vm_filter))
        self.clear()
        self.write('$FVM | Format-Table -Property Name, '
          'State -HideTableHeaders -AutoSize')
        self._vm_list = vmap.parse_vm_list(self.read())

        guru = []
        guru.append('Welcome, #%s!\r\n\r\nChoose a virtual machine '
          'to start working with:\r\n\r\n' %(self._token))
        for i, line in enumerate(self._vm_list, start = 1):
            guru.append('[%s] -------- %s -------- %s\r\n'
              %(str(i), line[0], line[1]))
        answer = "".join(guru)
        return answer

    def choose_vm(self, num):
        if num > 0 and num <= len(self._vm_list):
            self._chosen_vm = self._vm_list[num - 1][0]
            self.write('$CVM = $FVM | ? Name -EQ "%s"' %(self._chosen_vm))
            self.clear()
            return self._chosen_vm
        elif num == 0:
            self._chosen_vm = ''
            return ''
        else:
            return ''

    def vm_status(self):
        self.write('$CVM | select Name,State,CPUUsage,@{n="MemoryAssigned(GB)"'
          ';e={$_.MemoryAssigned/1gb}},@{n="MemoryDemand(GB)"'
          ';e={$_.MemoryDemand/1gb}},Uptime,@{n="IP"'
          ';e={$(($_.NetworkAdapters.IPAddresses) -join " , ")}}')
        return ('\t###STATUS###\n%s\n###restart, stop, start, shutdown, '
          'help###' %(vmap.parse_vm_status(self.read())))

    def manage_vm(self, command):
        key = ''
        if command != 'Start-VM':
        	key = ' -force'
        self.write('$CVM | %s%s' %(command, key))
        self.clear()

    def close(self):
        self._proc.kill()
