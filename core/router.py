import config


class Router:
    def __init__(self, chain):
        self.chain = chain()
        self.w3 = self.chain.get_web3_instance()
        self.private_key = config.private_key
