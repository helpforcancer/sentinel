import sys
import os
import io
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from misc import printdbg


class HelpforcancerConfig():

    @classmethod
    def slurp_config_file(self, filename):
        # read helpforcancer.conf config but skip commented lines
        f = io.open(filename)
        lines = []
        for line in f:
            if re.match('^\s*#', line):
                continue
            lines.append(line)
        f.close()

        # data is helpforcancer.conf without commented lines
        data = ''.join(lines)

        return data

    @classmethod
    def get_rpc_creds(self, data, network='mainnet'):
        # get rpc info from helpforcancer.conf
        match = re.findall(r'rpc(user|password|port)=(.*?)$', data, re.MULTILINE)

        # python >= 2.7
        creds = {key: value for (key, value) in match}

        # standard Helpforcancer defaults...
        default_port = 24127 if (network == 'mainnet') else 24131

        # use default port for network if not specified in helpforcancer.conf
        if not ('port' in creds):
            creds[u'port'] = default_port

        # convert to an int if taken from helpforcancer.conf
        creds[u'port'] = int(creds[u'port'])

        # return a dictionary with RPC credential key, value pairs
        return creds

    @classmethod
    def tokenize(self, filename):
        tokens = {}
        try:
            data = self.slurp_config_file(filename)
            match = re.findall(r'(.*?)=(.*?)$', data, re.MULTILINE)
            tokens = {key: value for (key, value) in match}
        except IOError as e:
            printdbg("[warning] error reading config file: %s" % e)

        return tokens
