
from boa.interop.System.Storage import *

from libs.SafeCheck import *


DEPLOYER = bytearray(
    b'\x15\xd7\x1d\x26\xc7\x22\x84\xc2\xf6\x46'
    b'\xff\x4f\xde\xfd\xae\xdc\x65\xdc\xfe\x8d'
)

OWNER_KEY = '___OWNER'
TOKEN_CONTRACT_KEY = '___TOKEN'


def Main(operation, args):
    return True


def Deploy(_tokenaddr):
    RequireWitness(DEPLOYER)

    ctx = GetContext()
    Put(ctx, TOKEN_CONTRACT_KEY, _tokenaddr)


def RegisterDistribution(_addresses, _fees, _closes, _maxes):
    """
    Distributes the token benefits to the distributors.
    :param _addresses: distributors' addresses array.
    :param _fees: distributors' fee percent array.
    :param _closes: distribution end time array.
    :param _maxes: maximum distributable tokens array.
    """
    pass


def RegisterPaper(_distributor, _address, _ipfsHash):
    """
    Registers a paper.
    :param _distributor:
    :param _address:
    :param _ipfsHash:
    :return:
    """
    pass

