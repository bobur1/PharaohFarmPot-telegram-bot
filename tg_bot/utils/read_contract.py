from web3 import Web3
from tg_bot.data.config import RPS, CONTRACT, abi
from tg_bot.data.database import get_wallet_user
import asyncio

def connecting():
    web3 = Web3(Web3.HTTPProvider(RPS))
    if not web3.is_connected():
        print('Error connecting!')
    elif web3.is_connected():
        return web3

def levels(user_id):
    contractAddress = connecting().to_checksum_address(CONTRACT)
    watch = connecting().eth.contract(address=contractAddress, abi=abi())
    wallet = get_wallet_user(user_id)
    lvl_1 = watch.functions.getLevel1Reffers(wallet).call()
    lvl_2 = watch.functions.getLevel2Reffers(wallet).call()
    lvl_3 = watch.functions.getLevel3Reffers(wallet).call()
    lvl_4 = watch.functions.getLevel4Reffers(wallet).call()
    lvl_5 = watch.functions.getLevel5Reffers(wallet).call()
    lvl_6 = watch.functions.getLevel6Reffers(wallet).call()
    lvl_7 = watch.functions.getLevel7Reffers(wallet).call()
    return {
        "lvl_1": len(lvl_1),
        "lvl_2": len(lvl_2),
        "lvl_3": len(lvl_3),
        "lvl_4": len(lvl_4),
        "lvl_5": len(lvl_5),
        "lvl_6": len(lvl_6),
        "lvl_7": len(lvl_7)
    }


def get_max_payout(user_id):
    contractAddress = connecting().to_checksum_address(CONTRACT)
    watch = connecting().eth.contract(address=contractAddress, abi=abi())
    wallet = get_wallet_user(user_id)
    payout = int(watch.functions.getMaxPayout(wallet).call()) / 1000000000000000000
    return payout

def get_user_intial_deposit(wallet):
    contractAddress = connecting().to_checksum_address(CONTRACT)
    watch = connecting().eth.contract(address=contractAddress, abi=abi())
    payout = watch.functions.user_data(wallet).call()
    initial_deposit = int(payout[2]) / 1000000000000000000
    return initial_deposit

# daily payout
def calculate_payout(user_id):
    contractAddress = connecting().to_checksum_address(CONTRACT)
    watch = connecting().eth.contract(address=contractAddress, abi=abi())
    wallet = get_wallet_user(user_id)
    contract_balance = int(watch.functions.getContractBalance().call()) / 1000000000000000000
    daily_payout_percentage = 0

    if contract_balance <= 2500000:
        daily_payout_percentage = 0.003
    elif contract_balance <= 5000000:
        daily_payout_percentage = 0.005
    elif contract_balance <= 10000000:
        daily_payout_percentage = 0.0075
    else:
        daily_payout_percentage = 0.01


    balance = int(watch.functions.user_data(wallet).call()[1]) / 1000000000000000000

    payout = daily_payout_percentage * balance
    return payout


def available_rewards(user_id):
    contractAddress = connecting().to_checksum_address(CONTRACT)
    watch = connecting().eth.contract(address=contractAddress, abi=abi())
    wallet = get_wallet_user(user_id)
    payout = int(watch.functions.availableRewards(wallet).call()) / 1000000000000000000
    return payout


def double_up(user_id):
    contractAddress = connecting().to_checksum_address(CONTRACT)
    watch = connecting().eth.contract(address=contractAddress, abi=abi())
    wallet = get_wallet_user(user_id)
    payout_0 = watch.functions.user_data(wallet).call()
    payout_1 = watch.functions.availableRewards(wallet).call()
    claimed = payout_0[4]
    available_rewards = payout_1
    max_payout = payout_0[3]
    counting = int(max_payout - (claimed + available_rewards)) / 1000000000000000000
    if claimed + available_rewards >= max_payout:
        return False
    else:
        return counting


def doubling_amount(user_id):
    contractAddress = connecting().to_checksum_address(CONTRACT)
    watch = connecting().eth.contract(address=contractAddress, abi=abi())
    wallet = get_wallet_user(user_id)
    payout_0 = watch.functions.user_data(wallet).call()
    payout_1 = int(watch.functions.depositAfterTax(payout_0[2] * 2).call()) / 1000000000000000000
    return payout_1 + 1
