import os

from dotenv import load_dotenv
from eth_account import Account

load_dotenv()

private_key = os.getenv('PRIVATE_KEY')
public_key = Account.from_key(private_key).address

