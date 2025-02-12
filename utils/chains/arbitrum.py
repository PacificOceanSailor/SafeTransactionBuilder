from . import Web3Address, Chain, MultiSendCallOnlyABI, SymmioTimeLockABI


class Arbitrum(Chain):
    rpc = 'https://arbitrum.llamarpc.com'
    id = 42161
    address_book = {
        'safe': {
            'MultiSendCallOnly': Web3Address(
                address='0x9641d764fc13c8B624c04430C7356C1C7C8102e2',
                abi=MultiSendCallOnlyABI)
        },
        'symmio': {
            'timelock': Web3Address(
                address='0x0CbF07176e67671C99222beBDB166EfC58dACD95',
                abi=SymmioTimeLockABI
            )
        }
    }

    def get_safe_tx_service_url(self, safe_address):
        return f'https://safe-transaction-arbitrum.safe.global/api/v1/safes/{safe_address}/multisig-transactions/'
