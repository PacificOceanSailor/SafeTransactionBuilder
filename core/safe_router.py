import json
from typing import List

import requests
from eth_account import Account
from eth_typing import URI
from safe_eth.eth import EthereumClient
from safe_eth.safe import Safe, SafeOperationEnum
from eth_abi import encode

from utils import abi_holder as ABIs
from core.timelock_router import TimeLockRouter
from utils.safe_encoder import encode_raw_tx
from core.router import Router
import constants as consts


class SafeRouter(Router):
    def __init__(self, chain, safe_address):
        super().__init__(chain)
        ethereum_client = EthereumClient(URI(self.chain.rpc))
        self.safe = Safe(address=self.w3.to_checksum_address(safe_address), ethereum_client=ethereum_client)
        timelock_address = self.chain.address_book['symmio']['timelock'].address
        timelock_abi = ABIs.SymmioTimeLockABI
        self.timelock_router = TimeLockRouter(chain, timelock_address, timelock_abi)

    @staticmethod
    def _build_data_get_val(raw_transactions: List[dict]):
        hex_data: str = ""
        total_value = 0
        for raw_tx in raw_transactions:
            hex_data += encode_raw_tx(raw_tx)
            total_value += raw_tx['value']
        return total_value, consts.multi_call_signature + encode(['bytes'], [bytes.fromhex(hex_data)]).hex()

    def create_bash(self, raw_transactions: List[dict], safe_nonce: int = None):
        if not safe_nonce:
            safe_nonce = self.get_nonce()
        account = Account.from_key(self.private_key)
        sender_address = self.w3.to_checksum_address(account.address)
        to_address = self.w3.to_checksum_address(self.chain.address_book['safe']['MultiSendCallOnly'].address)
        value, data = self._build_data_get_val(raw_transactions)
        operation = SafeOperationEnum.CALL.value

        safe_tx = self.safe.build_multisig_tx(
            to=to_address,
            value=value,
            data=data,
            operation=operation,
            safe_tx_gas=0,
            base_gas=0,
            gas_price=0,
            gas_token=self.w3.to_checksum_address('0x0000000000000000000000000000000000000000'),
            # Use ETH as gas token
            refund_receiver=sender_address,
            safe_nonce=safe_nonce
        )

        safe_tx_hash = safe_tx.safe_tx_hash.hex()
        safe_tx_data = {
            "safe": self.safe.address,
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
            "signature": '0x' + safe_tx.sign(self.private_key).hex(),
            "origin": sender_address
        }

        safe_tx_service_url = self.chain.get_safe_tx_service_url(self.safe.address)

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
            print(f'reason: {response.text}')
        return safe_tx.safe_nonce

    def get_nonce(self):
        return self.safe.retrieve_nonce()

    def schedule_timelock(self, raw_transactions: List[dict], safe_nonce=None, predecessor: int = 0, salt: int = 0):
        length: int = len(raw_transactions)
        scheduled_tx = self.timelock_router.schedule_tx(raw_transactions, length, predecessor, salt)
        self.create_bash([scheduled_tx], safe_nonce)

    def execute_timelock(self, raw_transactions: List[dict], safe_nonce=None, predecessor: int = 0, salt: int = 0):
        length: int = len(raw_transactions)
        execute_tx = self.timelock_router.execute_tx(raw_transactions, length, predecessor, salt)
        self.create_bash([execute_tx], safe_nonce)
