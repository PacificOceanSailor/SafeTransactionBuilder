import config


class Contract:
    def __init__(self, contract_address, contract_abi, w3):
        self.contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=contract_abi)
        self.w3 = w3
        self.pk = config.public_key

    def __getattr__(self, name):
        def method(*args, **kwargs):
            value = 0
            if "value" in kwargs.keys():
                value = kwargs.get("value")
            func_call = getattr(self.contract.functions, name)(*args)
            raw_tx = func_call.build_transaction({
                'from': self.pk,
                'value': value,
                'nonce': self.w3.eth.get_transaction_count(self.pk),
                'gasPrice': self.w3.eth.gas_price,
                'gas': 3000000000
            })
            return raw_tx
        return method
