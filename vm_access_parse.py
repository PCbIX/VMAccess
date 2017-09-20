import re

def read_cfg(token):
    with open('config.cfg', 'r') as config:
        cfg = config.readlines()
        for i, line in enumerate(cfg):
            if re.match('#' + token + '.*', line):
                res = []
                res.append(token)
                res.append(cfg[i + 1].split('$ClusterName = ', 1)[1].split()[0])
                res.append(cfg[i + 2].split('$VMFilter = ', 1)[1].split()[0])
                return res
        return None

def parse_vm_list(raw):
    if raw:
        result = []
        for line in raw[1:]:
            if not line.startswith('\n') and not line.startswith('\r\n'):
                result.append(line.split())
        return result
    return None

def parse_vm_status(raw):
    if raw:
        result = "".join(raw[1:])
        return result
    return 'Some error occurred while updating status!\r\n'