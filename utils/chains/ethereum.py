from . import Web3Address, Chain, MultiSendCallOnlyABI


class Ethereum(Chain):
    rpc = 'https://eth.llamarpc.com'
    id = 1
    address_book = {
        'safe': {
            'MultiSendCallOnly': Web3Address(
                address='0x9641d764fc13c8B624c04430C7356C1C7C8102e2',
                abi=MultiSendCallOnlyABI)
        }
    }

    def get_safe_tx_service_url(self, safe_address):
        return f'https://safe-transaction-mainnet.safe.global/api/v1/safes/{safe_address}/multisig-transactions/'
