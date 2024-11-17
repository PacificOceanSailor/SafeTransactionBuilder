import json
import requests
from web3 import Web3
from eth_account import Account
from safe_eth.safe import SafeOperationEnum
from safe_eth.safe import Safe
from safe_eth.eth import EthereumClient

w3 = Web3(Web3.HTTPProvider(f'https://ethereum-sepolia.blockpi.network/v1/rpc/public'))
ethereum_client = EthereumClient('https://ethereum-sepolia.blockpi.network/v1/rpc/public')

private_key = ''  # Replace with your private key
account = Account.from_key(private_key)
sender_address = account.address

safe_address = ''
safe = Safe(address=w3.to_checksum_address(safe_address), ethereum_client=ethereum_client)

to_address = ''
value = w3.to_wei(0.001, 'ether')
data = b''
operation = SafeOperationEnum.CALL.value

safe_tx = safe.build_multisig_tx(
    to=w3.to_checksum_address(to_address),
    value=value,
    data=data,
    operation=operation,
    safe_tx_gas=0,
    base_gas=0,
    gas_price=0,
    gas_token=w3.to_checksum_address('0x0000000000000000000000000000000000000000'),  # Use ETH as gas token
    refund_receiver=w3.to_checksum_address(sender_address)
)

safe_tx_hash = safe_tx.safe_tx_hash.hex()
safe_tx_data = {
    "safe": safe_address,
    "to": safe_tx.to,
    "value": str(safe_tx.value),
    "data": safe_tx.data.hex(),
    "operation": safe_tx.operation,
    "gasToken": safe_tx.gas_token,
    "safeTxGas": safe_tx.safe_tx_gas,
    "baseGas": safe_tx.base_gas,
    "gasPrice": safe_tx.gas_price,
    "refundReceiver": safe_tx.refund_receiver,
    "nonce": safe_tx.safe_nonce,
    "contractTransactionHash": safe_tx_hash,
    "sender": sender_address,
    "signature": '0x'+safe_tx.sign(private_key).hex(),
    "origin": w3.to_checksum_address(sender_address)
}

safe_tx_service_url = f'https://safe-transaction-sepolia.safe.global/api/v1/safes/{safe_address}/multisig-transactions/'

headers = {'Content-Type': 'application/json'}
response = requests.post(
    url=safe_tx_service_url,
    headers=headers,
    data=json.dumps(safe_tx_data)
)

if response.status_code == 201:
    print('Transaction submitted successfully.')
else:
    print('Failed to submit transaction.')
    print('Response:', response.text)




