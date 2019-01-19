import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from helpforcancerd import HelpforcancerDaemon
from helpforcancer_config import HelpforcancerConfig


def test_helpforcancerd():
    config_text = HelpforcancerConfig.slurp_config_file(config.helpforcancer_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000009701eb781a8113b1af1d814e2f060f6408a2c990db291bc5108a1345c1e'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000097c608165d389ccaf6b5a9534721b8c672b48ff1b966d9dd6d9413ab36b'

    creds = HelpforcancerConfig.get_rpc_creds(config_text, network)
    helpforcancerd = HelpforcancerDaemon(**creds)
    assert helpforcancerd.rpc_command is not None

    assert hasattr(helpforcancerd, 'rpc_connection')

    # Helpforcancer testnet block 0 hash == 0000097c608165d389ccaf6b5a9534721b8c672b48ff1b966d9dd6d9413ab36b
    # test commands without arguments
    info = helpforcancerd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert helpforcancerd.rpc_command('getblockhash', 0) == genesis_hash
