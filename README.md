# SafeTransactionBuilder
A user-friendly interface for creating bashes on Safe Wallet and signing them. It makes creating multiple transactions on multiple chains easy.
## Installaion
Running this command, the requirements of the project would be installed on you machine.
* ⚠️ caution: Do not install other version of the required packages. The project might not work due to incompatibility of some of the important packages *
```bash
pip install -r requirements.txt
```
## Configuration
You should create a .env file with a ```PRIVATE_KEY``` element in it. this key would be used to sign the bash.
## Running
The file that you can write your commands and use the project is ```interface.py```   
The project has two main classes, ```Contract``` and ```SafeRouter```. You should instantiate a ```Contract``` for each contract on a network that you want to interact with in the bash.    
Instantiating a ```SafeRouter``` gives a router to interact with Safe Waller on a single chain. Using a ```SafeRouter``` instance, you can send as many as bashes as you want, using the method ```SafeRouter::creat_bash```.   
Note that when you create a bash on safe, it should have a nonce; By default the nonce is the last executed bash/transaction on the wallet. You can get your nonce using ```SafeRouter::get_nonce``` and you should increase it by one if you want to send multiple bashes without executing the ones in the queue.   
Here is a sample usage of the project that creates a router on ```Sepolia``` network, instantiates three ```Contract``` instances and then creates three bashes with multiple contract interactions.

Also using ```SafeRouter:schedule_timelock``` and ```SafeRouter:execute_timelock``` you can schedule and execute on symmio_timelock. You don't have to set it up mannually, just specifying the network, it retrives the related addresses and abis from address book.
```Python
from core.contract import Contract
from core.safe_router import SafeRouter
from utils.chains.sepolia import Sepolia

safe_router = SafeRouter(chain=Sepolia, safe_address="<address of the wallet on Safe")

w3_instance = safe_router.chain.get_web3_instance()

#creating instances of contracts you want to interact with using safe router.
contract1 = Contract('<contract_address>', '<ABI>', w3_instance)
contract2 = Contract('<contract_address>', '<ABI>', w3_instance)
contract3 = Contract('<contract_address>', '<ABI>', w3_instance)

#getting safe nonce. You can use this for txs to queue in safe{wallet}.
nonce = safe_router.get_nonce()

#bash creation on safe{wallet}
safe_router.create_bash([contract1.seta("test"), contract1.seta("one")], nonce)
safe_router.create_bash([contract1.seta("second"), contract1.seta("wow"), contract3.set_sentence3("fire")], nonce+1)
safe_router.create_bash([contract2.set_sentence("your"), contract3.set_sentence3("my"), contract2.set_sentence("diamond")], nonce+2)

#timelock
safe_router.schedule_timelock([contract1.seta("test19")], nonce+3, 0, 174)
safe_router.execute_timelock([contract1.seta("test19")], nonce+4, 0, 174)
```
