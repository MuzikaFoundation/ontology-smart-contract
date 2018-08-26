from boa.interop.Ontology.Action import RegisterAction
from boa.interop.Ontology.Runtime import GetTrigger, CheckWitness
from boa.interop.Ontology.TriggerType import Application, Verification
from boa.interop.Ontology.Storage import *
from boa.interop.Ontology.Account import GetScriptHash
from boa.builtins import concat

from libs.SafeCheck import Require, RequireScriptHash, RequireWitness
from libs.Utils import SafePut
from libs.SafeMath import uSub


# Token Info
TOKEN_NAME = 'Muzika Coin'
TOKEN_SYMBOL = 'MZK'

INITIAL_SUPPLY = 1000000000
TOKEN_DECIMALS = 8
TOKEN_FACTOR = 100000000

# The deployer address of the token
TOKEN_DEPLOYER = 'AVLtVwA5gn3TFEwRSQMmXmFT6eXPnQznSq'

# Storage key constants
# Circulations: current total MZK supply.
TOKEN_CIRCULATION_KEY = 'MZK-circulation'

# Owner Script Hash : the script hash of the address for the owner
OWNER_KEY = 'MZK-Owner'


NEP5_METHODS = [
    'name',
    'symbol',
    'decimals',
    'totalSupply',
    'balanceOf',
    'transfer',
    'transferFrom',
    'approve',
    'allowance'
]

# Actions
OnTransfer = RegisterAction('transfer', 'addr_from', 'addr_to', 'amount')
OnApprove = RegisterAction('approve', 'addr_from', 'addr_to', 'amount')


def Deploy():
    ctx = GetContext()

    # if already deployed, cannot deploy again
    # even if the transaction sender is owner
    Require(Get(ctx, 'deployed') != 1)

    # the first owner is the deployer
    # the owner can transfer ownership to another
    owner = GetScriptHash(TOKEN_DEPLOYER)

    # the transaction sender must be deployer
    RequireWitness(owner)

    # transfer ownership to the deployer
    Put(ctx, OWNER_KEY, owner)

    # Give all tokens to the owner
    Put(ctx, owner, INITIAL_SUPPLY * TOKEN_FACTOR)
    Put(ctx, 'deployed', 1)
    return True


def Main(operation, args):
    trigger = GetTrigger()

    if trigger == Verification():
        ctx = GetContext()
        owner = Get(ctx, OWNER_KEY)

        # if owner is not registered yet, the owner is deployer
        if not owner:
            owner = GetScriptHash(TOKEN_DEPLOYER)

        if CheckWitness(owner):
            return True
        return False

    elif trigger == Application():
        if operation == 'deploy':
            return Deploy()

        elif operation == 'name':
            return TOKEN_NAME

        elif operation == 'symbol':
            return TOKEN_SYMBOL

        elif operation == 'decimals':
            return TOKEN_DECIMALS

        elif operation == 'totalSupply':
            return Get(GetContext(), TOKEN_CIRCULATION_KEY)

        elif operation == 'balanceOf':
            if len(args) == 1:
                return BalanceOf(args[0])

        elif operation == 'transfer':
            if len(args) == 3:
                return Transfer(args[0], args[1], args[2])

        elif operation == 'transferFrom':
            if len(args) == 3:
                return TransferFrom(args[0], args[1], args[2])

        elif operation == 'approve':
            if len(args) == 3:
                return Approve(args[0], args[1], args[2])

        elif operation == 'allowance':
            if len(args) == 2:
                return Allowance(args[0], args[1])

    return False


def BalanceOf(account):
    if len(account) != 20:
        return 0

    return Get(GetContext(), account)


def Transfer(t_from, t_to, amount):
    ctx = GetContext()

    Require(amount > 0)               # cannot transfer minus value
    RequireScriptHash(t_to)           # receiver address validation
    RequireWitness(t_from)            # transaction sender should be sender
    Require(t_from != t_to)           # sender and receiver cannot be the same

    # calculate after from-account value and to-account value
    from_val = uSub(Get(ctx, t_from), amount)
    to_val = Get(ctx, t_to) + amount

    # put from and to account result value
    SafePut(ctx, t_from, from_val)
    Put(ctx, t_to, to_val)

    OnTransfer(t_from, t_to, amount)
    return True


def TransferFrom(t_from, t_to, amount):
    ctx = GetContext()

    Require(amount > 0)               # cannot transfer minus value
    RequireScriptHash(t_from)         # sender address validation
    RequireScriptHash(t_to)           # receiver address validation

    approve_key = concat(t_from, t_to)
    approve_val = Get(ctx, approve_key)
    from_val = Get(ctx, t_from)
    to_val = Get(ctx, t_to)

    Require(amount <= approve_val)
    Require(approve_val <= from_val)
    Require(from_val >= approve_val)

    SafePut(ctx, t_from, from_val - amount)
    SafePut(ctx, t_to, to_val + amount)
    SafePut(ctx, approve_key, approve_val - amount)
    return True


def Approve(t_from, t_to, amount):
    ctx = GetContext()

    Require(amount >= 0)
    RequireScriptHash(t_from)
    RequireScriptHash(t_to)
    RequireWitness(t_from)

    from_val = Get(ctx, t_from)

    Require(from_val >= amount)
    approve_key = concat(t_from, t_to)

    SafePut(ctx, approve_key, amount)
    OnApprove(t_from, t_to, amount)
    return True


def Allowance(t_from, t_to):
    return Get(GetContext(), concat(t_from, t_to))
