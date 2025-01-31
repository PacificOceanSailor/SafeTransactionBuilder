from core.contract import Contract
from core.safe_router import SafeRouter
from utils.chains.sepolia import Sepolia

# Example usage
safe_router = SafeRouter(chain=Sepolia, safe_address="")

w3_instance = safe_router.chain.get_web3_instance()

#creating instances of contracts you want to interact with using safe router.
# contract1 = Contract('<contract_address>', '<ABI>', w3_instance)
# contract2 = Contract('<contract_address>', '<ABI>', w3_instance)
# contract3 = Contract('<contract_address>', '<ABI>', w3_instance)

#getting safe nonce. You can use this for txs to queue in safe{wallet}.
# nonce = safe_router.get_nonce()

#bash creation on safe{wallet}
# safe_router.create_bash([contract1.seta("test"), contract1.seta("one")])
# safe_router.create_bash([contract1.set_sentence("second"), contract1.set_sentence("wow"), contract3.set_sentence3("fire")], nonce)
# safe_router.create_bash([contract2.set_sentence("your"), contract3.set_sentence3("my"), contract2.set_sentence("diamond")], nonce+1)

#timelockgi
# safe_router.schedule_timelock([contract1.seta("test19")], nonce, 0, 174)
# safe_router.execute_timelock([contract1.seta("test19")], nonce+1, 0, 174)
