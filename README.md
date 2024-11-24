# SafeTransactionBuilder
A user-friendly interface for creating bashes on Safe Wallet and signing them. It makes creating multiple transaction on multiple chains easy.
## Installaion
Running this command the requirements of the project would be installed on you machine.
* ⚠️ caution: Do not install other version of the required packages. The project might not work due to incompatibility of some of the important packages *
```bash
pip install -r requirements.txt
```
## Configuration
You should create a .env file with a ```PRIVATE_KEY``` element in it. this key would be used to sign the bash.
## Running
The file that you can write your commands and use the project is ```interface.py```   
The project has to main classes, ```Contract``` and ```SafeRouter```. You should instantiate a ```Contract``` for each contract on a network that you want to interact with in the bash.    
Instantiating a ```SafeRouter``` gives a router to interact with Safe Waller on a single chain. Using a ```SafeRouter``` instance, you can send as many as bashes as you want using the method ```SafeRouter::creat_bash```.   
Note that when you create a bash on safe, it should have a nonce; By default the nonce is the last confiremed bash/transaction on the wallet. You can get your nonce using ```SafeRouter::get_nonce``` and you should increase it if you want to send multiple bashes without executing the ones in the queue.   
Here is a sample usage of the project that creates a router on ```Sepolia``` network, instantiates three ```Contract``` instances and then creates three bashes with multiple contract interactions.
```Python
from core.contract import Contract
from core.safe_router import SafeRouter
from utils.chains.sepolia import Sepolia

safe_router = SafeRouter(chain=Sepolia, safe_address="<address of the wallet on Safe")

w3_instance = safe_router.chain.get_web3_instance()

contract1 = Contract("<ContractAddress>", "<ABI>", w3_instance)
contract2 = Contract("<ContractAddress>", "<ABI>", w3_instance)
contract3 = Contract("<ContractAddress>", "<ABI>", w3_instance)

nonce = safe_router.get_nonce()

safe_router.create_bash([contract3.set_sentence3("test"), contract2.set_sentence("one")])
safe_router.create_bash([contract1.set_sentence("second"), contract1.set_sentence("wow"), contract3.set_sentence3("fire")], nonce+1)
safe_router.create_bash([contract2.set_sentence("your"), contract3.set_sentence3("my"), contract2.set_sentence("diamond")], nonce+2)
```
