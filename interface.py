from core.contract import Contract
from core.safe_router import SafeRouter
from utils.chains.sepolia import Sepolia

# Example usage
safe_router = SafeRouter(chain=Sepolia, safe_address="")

w3_instance = safe_router.chain.get_web3_instance()

contract1 = Contract("", '[{"inputs":[],"name":"get_sentence","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_sen","type":"string"}],"name":"set_sentence","outputs":[],"stateMutability":"payable","type":"function"}]', w3_instance)
contract2 = Contract("", '[{"inputs":[],"name":"get_sentence","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_sen","type":"string"}],"name":"set_sentence","outputs":[],"stateMutability":"payable","type":"function"}]', w3_instance)
contract3 = Contract("", '[{"inputs":[{"internalType":"string","name":"_sen","type":"string"}],"name":"set_sentence3","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"get_sentence2","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]', w3_instance)

nonce = safe_router.get_nonce()

safe_router.create_bash([contract3.set_sentence3("test"), contract2.set_sentence("one")])
safe_router.create_bash([contract1.set_sentence("second"), contract1.set_sentence("wow"), contract3.set_sentence3("fire")], nonce+1)
safe_router.create_bash([contract2.set_sentence("your"), contract3.set_sentence3("my"), contract2.set_sentence("diamond")], nonce+2)
