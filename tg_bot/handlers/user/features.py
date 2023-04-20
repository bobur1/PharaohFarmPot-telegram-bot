from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tg_bot.data.config import info_message, RPS, CONTRACT, abi, MORALIS_API_KEY, MORALIS_CHAIN, BSC_API_KEY
from tg_bot.data.database import get_wallet_user, add_user_wallet, get_user_ids
from tg_bot.data.loader import dp, bot, scheduler

from tg_bot.keyboards.user.inline import info_callback, get_choice_info, choice_next, get_choice_wallet, \
    get_choice_wallet_cancel, get_choice_wallet_edit
from tg_bot.misc.states import AddWalletUser
from tg_bot.utils.read_contract import levels, get_max_payout, calculate_payout, available_rewards, double_up, \
    get_user_intial_deposit
from tg_bot.handlers.user.apshed import double_up_alert_users
from web3 import Web3
from web3.middleware import geth_poa_middleware
import asyncio
import requests
import json
from moralis import evm_api

web3 = Web3(Web3.HTTPProvider(RPS))
prev_block_number = 0
web3.middleware_onion.inject(geth_poa_middleware, layer=0)


contractAddress = web3.to_checksum_address(CONTRACT)
contract = web3.eth.contract(address=contractAddress, abi=abi())

api_key = MORALIS_API_KEY
reffered_body = {
  "anonymous": False,
  "inputs": [
    {
      "indexed": True,
      "internalType": "address",
      "name": "_referrer",
      "type": "address"
    },
    {
      "indexed": True,
      "internalType": "address",
      "name": "referred",
      "type": "address"
    },
    {
      "indexed": False,
      "internalType": "uint256",
      "name": "value",
      "type": "uint256"
    }
  ],
  "name": "Reffered",
  "type": "event"
}

referral_rewarded_body = {
  "anonymous": False,
  "inputs": [
    {
      "indexed": True,
      "internalType": "address",
      "name": "from",
      "type": "address"
    },
    {
      "indexed": False,
      "internalType": "address",
      "name": "to",
      "type": "address"
    },
    {
      "indexed": False,
      "internalType": "uint256",
      "name": "amount",
      "type": "uint256"
    }
  ],
  "name": "ReferralRewarded",
  "type": "event"
}

# define function to handle events and print to the console
def handle_event(event):
    print(Web3.toJSON(event))
    # and whatever

async def listener():
    chain = MORALIS_CHAIN
    global prev_block_number
    # delay 6 blocks in order to binance scan api to save events
    block_number = web3.eth.block_number - 6
    # block_number = 29078775
    # block_number = prev_block_number

    if prev_block_number == 0:
        prev_block_number = block_number
    else:
        if(prev_block_number > block_number):
            return
        print(f"--- watching blocks from {prev_block_number} to {block_number} --->")
        binance_api_key = BSC_API_KEY

        binance_api_url = ""

        if chain == 'bsc':
            binance_api_url = "api.bscscan.com"
        else:
            binance_api_url = "api-testnet.bscscan.com"

        url = f"https://{binance_api_url}/api?module=account&action=txlist&address={contractAddress}&startblock={prev_block_number}&endblock={block_number}&page=1&offset=1000&sort=asc&txtype=success&apikey={binance_api_key}"

        response = requests.get(url)
        data = json.loads(response.text)

        if data['status'] == '1':
            successful_transactions = [tx for tx in data['result'] if tx['isError'] == '0']
            double_up_tx_hash = []
            deposit_tx_hash = []
            for tx in successful_transactions:
                # doubleUp() - method id is '0x98c3e1dc'
                if tx['methodId'] == '0x98c3e1dc':
                    print("double up event hashed")
                    double_up_tx_hash.append(tx["hash"])

                # Deposit - method id is '0x6e553f65'
                elif tx['methodId'] == '0x6e553f65':
                    print("reffered event hashed")
                    deposit_tx_hash.append(tx["hash"])

            # Reffered rewarded emits here
            reffered_rewarded_params = {
                "chain": chain,
                "from_block": prev_block_number,
                "to_block": block_number,
                "topic": "0xb2dee5f49e7a09a5d7c95cd4dd5dc6410eea65d4e14519d6d3a6e14c8cf0e0e9",
                "address": contractAddress
            }

            result = evm_api.events.get_contract_events(
                api_key=api_key,
                body=referral_rewarded_body,
                params=reffered_rewarded_params,
            )

            print(len(result) > 0)
            if len(result["result"]) > 0:
                for res in result["result"]:
                    if res['transaction_hash'] in double_up_tx_hash:
                        team_member_wallet = web3.to_checksum_address(res["data"]["from"])
                        reward_amount = int(res["data"]["amount"]) / 1000000000000000000
                        reffered_wallet = web3.to_checksum_address(res["data"]["to"])
                        user_ids = get_user_ids(reffered_wallet)
                        if len(user_ids) > 0:
                            message_txt = f'<b>TEAM MEMBER DOUBLE UP!!!💰</b>\n\nWallet: <a href="https://bscscan.com/address/{team_member_wallet}">{team_member_wallet[0:6]}...{team_member_wallet[36:43]}</a>\n'
                            for user_id in user_ids:
                                lvl = levels(user_id)
                                max_payout = get_max_payout(user_id)
                                daily_payout = calculate_payout(user_id)
                                available = available_rewards(user_id)
                                double = double_up(user_id)
                                txt = message_txt + f'Your reward amount: {float(reward_amount):.2f} CAF\n\n📅Your Daily Payout: {float(daily_payout):.2f}  CAF\n💰Max Payout: {float(max_payout):.2f} CAF\n🎁Available Rewards: {float(available):.2f} CAF\n\nAmount of T1 referrals: {lvl["lvl_1"]}\nAmount of T2 referrals: {lvl["lvl_2"]}\nAmount of T3 referrals: {lvl["lvl_3"]}\nAmount of T4 referrals: {lvl["lvl_4"]}\nAmount of T5 referrals: {lvl["lvl_5"]}\nAmount of T6 referrals: {lvl["lvl_6"]}\nAmount of T7 referrals: {lvl["lvl_7"]}\n\n⏫How many CAF left until Double Up: {float(double):.2f} CAF'
                                await send_message_to_user(user_id, txt)

            # Reffered events catcher
            reffered_params = {
                "chain": chain,
                "from_block": prev_block_number,
                "to_block": block_number,
                "topic": "0x9a928c90e1ea9f4f5f10c2008f982ba23cc5e791c2152a33f534b021ea14eaa7",
                "address": contractAddress
            }

            result = evm_api.events.get_contract_events(
                api_key=api_key,
                body=reffered_body,
                params=reffered_params,
            )

            print(len(result) > 0)
            if len(result["result"]) > 0:
                for res in result["result"]:
                    if res['transaction_hash'] in deposit_tx_hash:
                        new_team_member_wallet = web3.to_checksum_address(res["data"]["_referrer"])
                        new_team_member_deposit_amount = get_user_intial_deposit(new_team_member_wallet)
                        reward_amount = int(res["data"]["value"]) / 1000000000000000000
                        reffered_wallet = web3.to_checksum_address(res["data"]["referred"])
                        user_ids = get_user_ids(reffered_wallet)
                        if len(user_ids) > 0:
                            message_txt = f'<b>TEAM MEMBER DEPOSIT!!!💰</b>\n\nWallet: <a href="https://bscscan.com/address/{new_team_member_wallet}">{new_team_member_wallet[0:6]}...{new_team_member_wallet[36:43]}</a>\nAmount: {float(new_team_member_deposit_amount):.2f} CAF '
                            for user_id in user_ids:
                                lvl = levels(user_id)
                                max_payout = get_max_payout(user_id)
                                daily_payout = calculate_payout(user_id)
                                available = available_rewards(user_id)
                                double = double_up(user_id)
                                txt = message_txt + f'\nYour reward amount: {float(reward_amount):.2f} CAF\n\n📅Your Daily Payout: {float(daily_payout):.2f}  CAF\n💰Max Payout: {float(max_payout):.2f} CAF\n🎁Available Rewards: {float(available):.2f} CAF\n\nAmount of T1 referrals: {lvl["lvl_1"]}\nAmount of T2 referrals: {lvl["lvl_2"]}\nAmount of T3 referrals: {lvl["lvl_3"]}\nAmount of T4 referrals: {lvl["lvl_4"]}\nAmount of T5 referrals: {lvl["lvl_5"]}\nAmount of T6 referrals: {lvl["lvl_6"]}\nAmount of T7 referrals: {lvl["lvl_7"]}\n\n⏫How many CAF left until Double Up: {float(double):.2f} CAF'
                                await send_message_to_user(user_id, txt)

        prev_block_number = block_number + 1

scheduler.add_job(listener, 'interval', seconds=3)

# Use the send_message method to send the message to the user
async def send_message_to_user(user_id: int, message_text: str):
    await bot.send_message(chat_id=user_id, text=message_text, disable_web_page_preview=True)

@dp.callback_query_handler(text_startswith='info')
async def first_page_handler_info(call: CallbackQuery):
    data = info_message()['info'][0]
    await call.message.edit_text(text=f'{data}', reply_markup=get_choice_info())


@dp.callback_query_handler(info_callback.filter())
async def page_handler_info(call: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    try:
        data = info_message()['info'][page]
        await call.message.edit_text(text=f'{data}', reply_markup=get_choice_info(page))
    except Exception:
        pass


@dp.message_handler(commands=['help'])
async def main_start(message: Message):
    await message.delete()
    await message.answer(text='<b>What can this bot do?</b>\n\nCommands:\n/start - Start the Bot\n/register_wallet - '
                              'Register your Account\n/stats - Check your Pharaoh Farm Ptot Stats of your registered '
                              'wallet', reply_markup=choice_next())


@dp.callback_query_handler(text_startswith='check_account')
async def check_account(call: CallbackQuery):
    if not get_wallet_user(user_id=call.message.chat.id):
        await call.message.edit_text(text='👇<b>Send me your <u>binance smart chain</u> wallet</b>', reply_markup=get_choice_wallet_cancel())
        await AddWalletUser.text.set()
    else:
        await call.message.edit_text(text='⌛️')
        lvl = levels(call.message.chat.id)
        max_payout = get_max_payout(call.message.chat.id)
        daily_payout = calculate_payout(call.message.chat.id)
        available = available_rewards(call.message.chat.id)
        double = double_up(call.message.chat.id)
        await call.message.edit_text(text=f'<b>Your Pharaohs farm pot statistics:</b>\n\n\n📅Your Daily Payout: {float(daily_payout):.2f}  CAF\n💰Max Payout: {float(max_payout):.2f} CAF\n🎁Available Rewards: {float(available):.2f} CAF\n\nAmount of T1 referrals: {lvl["lvl_1"]}\nAmount of T2 referrals: {lvl["lvl_2"]}\nAmount of T3 referrals: {lvl["lvl_3"]}\nAmount of T4 referrals: {lvl["lvl_4"]}\nAmount of T5 referrals: {lvl["lvl_5"]}\nAmount of T6 referrals: {lvl["lvl_6"]}\nAmount of T7 referrals: {lvl["lvl_7"]}\n\n⏫How many CAF left until Double Up: {float(double):.2f} CAF', reply_markup=choice_next())


@dp.message_handler(commands=['stats'])
async def check_account(message: Message):
    if not get_wallet_user(user_id=message.chat.id):
        await message.answer(text='👇<b>Send me your <u>binance smart chain</u> wallet</b>', reply_markup=get_choice_wallet_cancel())
        await AddWalletUser.text.set()
    else:
        await message.delete()
        msg = await message.answer(text='⌛️️')
        lvl = levels(message.chat.id)
        max_payout = get_max_payout(message.chat.id)
        daily_payout = calculate_payout(message.chat.id)
        available = available_rewards(message.chat.id)
        double = double_up(message.chat.id)
        await msg.delete()
        await message.answer(text=f'<b>Your Pharaohs farm pot statistics:</b>\n\n\n📅Your Daily Payout: {float(daily_payout):.2f}  CAF\n💰Max Payout: {float(max_payout):.2f} CAF\n🎁Available Rewards: {float(available):.2f} CAF\n\nAmount of T1 referrals: {lvl["lvl_1"]}\nAmount of T2 referrals: {lvl["lvl_2"]}\nAmount of T3 referrals: {lvl["lvl_3"]}\nAmount of T4 referrals: {lvl["lvl_4"]}\nAmount of T5 referrals: {lvl["lvl_5"]}\nAmount of T6 referrals: {lvl["lvl_6"]}\nAmount of T7 referrals: {lvl["lvl_7"]}\n\n⏫How many CAF left until Double Up: {float(double):.2f} CAF', reply_markup=choice_next())


@dp.message_handler(commands=['register_wallet'])
async def check_account(message: Message):
    await message.delete()
    if not get_wallet_user(user_id=message.chat.id):
        await message.answer(text='👇<b>Send me your <u>binance smart chain</u> wallet</b>', reply_markup=get_choice_wallet_cancel())
        await AddWalletUser.text.set()
    else:
        # await message.answer(text=f'❗<b>You have already added a wallet</b>\n\nWallet added earlier:\n<code>{get_wallet_user(message.chat.id)}</code>', reply_markup=get_choice_wallet_cancel())
        # await AddWalletUser.text.set()
        await message.answer(text=f'❗<b>You have already added a wallet</b>\n\nWallet added earlier:\n<code>{get_wallet_user(message.chat.id)}</code>\n\n👇<b>For edit exisiting wallet - send me your new <u>binance smart chain</u> wallet</b>', reply_markup=get_choice_wallet_cancel())
        await AddWalletUser.text.set()

@dp.message_handler(state=AddWalletUser.text)
async def change__text(message: Message, state: FSMContext):
    wallet = message.text
    await state.update_data(wallet=wallet)
    await message.delete()
    await message.answer(
        text=f'<b>Your Wallet</b>\n\n{wallet}\n\n<b> If you made a mistake in the text or changed your mind about '
             f'editing, press ❌ Cancel\nAnd repeat the procedure all over again</b>',
        reply_markup=get_choice_wallet())
    await AddWalletUser.wallet_state.set()

@dp.callback_query_handler(text_startswith='done_wallet_add_user', state=AddWalletUser.wallet_state)
async def start_change__text_text(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    wallet = data.get("wallet")

    if web3.is_address(wallet):
        wallet = web3.to_checksum_address(wallet)
        add_user_wallet(user_id=call.message.chat.id, wallet=wallet)
        await state.finish()
        await call.message.delete()
        await call.message.answer(text='<b>✅ Wallet successfully added</b>', reply_markup=choice_next())
        scheduler.add_job(double_up_alert_users, trigger='interval', seconds=5,
                        kwargs={'bot': bot, 'chat_id': call.message.chat.id})
    else:
        await state.finish()
        await call.message.delete()
        await call.message.answer(
        text=f'<b>❗Wrong wallet address❗</b>\n<b> Repeat the procedure all over again</b>',
             reply_markup=choice_next())

@dp.callback_query_handler(text_startswith='exit_states',state=[AddWalletUser.text, AddWalletUser.wallet_state])
async def fruit_page_handler(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text="❌ Cancel", reply_markup=choice_next())
