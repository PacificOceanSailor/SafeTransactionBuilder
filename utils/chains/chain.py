from web3 import Web3


class Web3Address:
    def __init__(self, address, abi):
        self.address = address
        self.abi = abi


class Chain:
    id: int
    rpc: str
    address_book: dict[str:dict[str:Web3Address]]

    @classmethod
    def get_web3_instance(cls):
        return Web3(Web3.HTTPProvider(cls.rpc))

    @classmethod
    def get_safe_tx_service_url(self, safe_address):
        pass