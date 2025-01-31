from . import Web3Address, Chain, MultiSendCallOnlyABI, SymmioTimeLockABI


class Sepolia(Chain):
    rpc = 'https://sepolia.drpc.org'
    id = 11155111

    address_book = {
        'safe': {
            'MultiSendCallOnly': Web3Address(
                address='0x9641d764fc13c8B624c04430C7356C1C7C8102e2',
                abi=MultiSendCallOnlyABI
            ),
        },
        'symmio': {
            'timelock': Web3Address(
                address='0x00b548d5150e451C56bE4e2B0809c17495f6DDDC',
                abi=SymmioTimeLockABI
            )
        }
    }

    def get_safe_tx_service_url(self, safe_address):
        return f'https://safe-transaction-sepolia.safe.global/api/v1/safes/{safe_address}/multisig-transactions/'
