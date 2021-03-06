import pytest
import sys
import os
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))


@pytest.fixture
def valid_helpforcancer_address(network='mainnet'):
    return 'TXDSaTXerg68SCyLkWw2ERsqoTMWRBZiZQ' if (network == 'testnet') else 'PGQuyQ6rtG5XSVe1bXbR7PdghpAZQEYdus'


@pytest.fixture
def invalid_helpforcancer_address(network='mainnet'):
    return 'TXDSaTXerg68SCyLkWw2ERsqoTMWRBZiZr' if (network == 'testnet') else 'PGQuyQ6rtG5XSVe1bXbR7PdghpAZQEYdut'


@pytest.fixture
def current_block_hash():
    return '000001c9ba1df5a1c58a4e458fb6febfe9329b1947802cd60a4ae90dd754b534'


@pytest.fixture
def mn_list():
    from masternode import Masternode

    masternodelist_full = {
        u'701854b26809343704ab31d1c45abc08f9f83c5c2bd503a9d5716ef3c0cda857-1': u'  ENABLED 70201 TPk18vGsifBT9Zcf4jExSvSfSnFLzBo4JS 1474157572    82842 1474152618  71111 52.90.74.124:24130',
        u'f68a2e5d64f4a9be7ff8d0fbd9059dcd3ce98ad7a19a9260d1d6709127ffac56-1': u'  ENABLED 70201 TLErYAESrr1b3zEEebX3kegLB1Udyg1bsp 1474157732  1590425 1474155175  71122 [2604:a880:800:a1::9b:0]:24130',
        u'656695ed867e193490261bea74783f0a39329ff634a10a9fb6f131807eeca744-1': u'  ENABLED 70201 TH6yFywNnZn9NDumfGrpLR8uX2FTK91isA 1474157704   824622 1474152571  71110 178.62.203.249:24130',
    }

    mnlist = [Masternode(vin, mnstring) for (vin, mnstring) in masternodelist_full.items()]

    return mnlist


@pytest.fixture
def mn_status_good():
    # valid masternode status enabled & running
    status = {
        "vin": "CTxIn(COutPoint(f68a2e5d64f4a9be7ff8d0fbd9059dcd3ce98ad7a19a9260d1d6709127ffac56, 1), scriptSig=)",
        "service": "[2604:a880:800:a1::9b:0]:24130",
        "pubkey": "PGQuyQ6rtG5XSVe1bXbR7PdghpAZQEYdus",
        "status": "Masternode successfully started"
    }
    return status


@pytest.fixture
def mn_status_bad():
    # valid masternode but not running/waiting
    status = {
        "vin": "CTxIn(COutPoint(0000000000000000000000000000000000000000000000000000000000000000, 4294967295), coinbase )",
        "service": "[::]:0",
        "status": "Node just started, not yet activated"
    }
    return status


# ========================================================================


def test_valid_helpforcancer_address():
    from helpforcancerlib import is_valid_helpforcancer_address

    main = valid_helpforcancer_address()
    test = valid_helpforcancer_address('testnet')

    assert is_valid_helpforcancer_address(main) is True
    assert is_valid_helpforcancer_address(main, 'mainnet') is True
    assert is_valid_helpforcancer_address(main, 'testnet') is False

    assert is_valid_helpforcancer_address(test) is False
    assert is_valid_helpforcancer_address(test, 'mainnet') is False
    assert is_valid_helpforcancer_address(test, 'testnet') is True


def test_invalid_helpforcancer_address():
    from helpforcancerlib import is_valid_helpforcancer_address

    main = invalid_helpforcancer_address()
    test = invalid_helpforcancer_address('testnet')

    assert is_valid_helpforcancer_address(main) is False
    assert is_valid_helpforcancer_address(main, 'mainnet') is False
    assert is_valid_helpforcancer_address(main, 'testnet') is False

    assert is_valid_helpforcancer_address(test) is False
    assert is_valid_helpforcancer_address(test, 'mainnet') is False
    assert is_valid_helpforcancer_address(test, 'testnet') is False


def test_deterministic_masternode_elections(current_block_hash, mn_list):
    winner = elect_mn(block_hash=current_block_hash, mnlist=mn_list)
    assert winner == 'f68a2e5d64f4a9be7ff8d0fbd9059dcd3ce98ad7a19a9260d1d6709127ffac56-1'

    winner = elect_mn(block_hash='00000056bcd579fa3dc9a1ee41e8124a4891dcf2661aa3c07cc582bfb63b52b9', mnlist=mn_list)
    assert winner == '656695ed867e193490261bea74783f0a39329ff634a10a9fb6f131807eeca744-1'


def test_deterministic_masternode_elections(current_block_hash, mn_list):
    from helpforcancerlib import elect_mn

    winner = elect_mn(block_hash=current_block_hash, mnlist=mn_list)
    assert winner == 'f68a2e5d64f4a9be7ff8d0fbd9059dcd3ce98ad7a19a9260d1d6709127ffac56-1'

    winner = elect_mn(block_hash='00000056bcd579fa3dc9a1ee41e8124a4891dcf2661aa3c07cc582bfb63b52b9', mnlist=mn_list)
    assert winner == '656695ed867e193490261bea74783f0a39329ff634a10a9fb6f131807eeca744-1'


def test_parse_masternode_status_vin():
    from helpforcancerlib import parse_masternode_status_vin
    status = mn_status_good()
    vin = parse_masternode_status_vin(status['vin'])
    assert vin == 'f68a2e5d64f4a9be7ff8d0fbd9059dcd3ce98ad7a19a9260d1d6709127ffac56-1'

    status = mn_status_bad()
    vin = parse_masternode_status_vin(status['vin'])
    assert vin is None


def test_hash_function():
    import helpforcancerlib
    sb_data_hex = '7b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a20225458445361545865726736385343794c6b577732455273716f544d5752425a695a517c5444577a394b664d6f3535777a6a32627262676158786e447a32386e416264506359222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d'
    sb_hash = 'cad371468b3f12c7390911ddf8358c6bfaa685ab6f39e26677888fd12f212a93'

    hex_hash = "%x" % helpforcancerlib.hashit(sb_data_hex)
    assert hex_hash == sb_hash


def test_blocks_to_seconds():
    import helpforcancerlib
    from decimal import Decimal

    precision = Decimal('0.001')
    assert Decimal(helpforcancerlib.blocks_to_seconds(0)) == Decimal(0.0)
    assert Decimal(helpforcancerlib.blocks_to_seconds(2)).quantize(precision) \
        == Decimal(314.4).quantize(precision)
    assert int(helpforcancerlib.blocks_to_seconds(16616)) == 2612035
