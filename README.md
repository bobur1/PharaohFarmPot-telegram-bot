# PharaohFarmPot Telegram Bot
## Introduction

This is a README file for the PharaohFarmPot Telegram Bot, which helps users track the PharaohFarmPot contract. The bot is implemented using Python, aiogram library for Telegram Bot, and pymongo library for MongoDB. It also uses the default RPC from Binance and Moralis solution to track events such as "Referred" and "ReferredRewarded".

## Prerequisites

Before you proceed with the setup, please ensure you have the following software installed:

Python 3.6 or higher: Download and install Python from https://www.python.org/downloads/.
Poetry 1.4.2: A tool for dependency management and packaging in Python. Install it by following the instructions at https://python-poetry.org/docs/#installation.

## Installation

Follow these steps to set up the PharaohFarmPot Telegram Bot:

- Clone the repository:

```sh
git clone REPO_LINK
cd pharaohfarm_pot_bot
```

- Install dependencies using Poetry:
```sh
poetry install
```

- Configure the database connection by updating the `tg_bot/data/database.py` file. Ensure you have a MongoDB instance running and provide the appropriate connection details (e.g., host, port, database name, and credentials).

- Set up your bot token and other required environment variables by creating a `.env`(use .env-example) file in the project root with the following content:
```sh
RPS="https://bsc-dataseed3.binance.org/" #your_binance_rpc_url
TOKEN="" # your_telegram_api_token
CONTRACT="" # PharaohFarmPot contract address
MORALIS_API_KEY="" # your_moralis_api_key
MORALIS_CHAIN="bsc" # "bsc" - for binance mainnet; "bsc test" - for the testnet
```
Replace the placeholders with your actual API keys and URLs.

- Run the bot using the following command:
```sh
poetry run python main.py
```

## MongoDB Table Structure
The MongoDB table for clients has the following structure:

```sh
{
   "_id": "user_id",
   "user_id": "str(user_id)",
   "user_name": "str(user_name)",
   "wallet": false
}
```

This structure is used for storing user information, such as their Telegram user ID, username, and wallet status.

## Contributing
If you would like to contribute to the project, please submit a pull request or open an issue on the repository page.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.