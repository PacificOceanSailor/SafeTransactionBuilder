from typing import List

from core.router import Router
from core.contract import Contract
from utils.handy_functions import split_by


class TimeLockRouter(Router):
    def __init__(self, chain, address, abi):
        super().__init__(chain)
        self.time_lock_controller = Contract(self.chain.address_book['symmio']['timelock'].address,
                                             self.chain.address_book['symmio']['timelock'].abi,
                                             self.chain.get_web3_instance())

    def schedule_tx(
            self, raw_transactions: List[dict], length: int, predecessor: int = 0, salt: int = 0, delay: int = 0
    ):
        schedule_tx = None
        if delay == 0:
            delay = self.time_lock_controller.contract.functions.getMinDelay().call()
        if length == 1:
            raw_tx = raw_transactions[0]
            schedule_tx = self.time_lock_controller.schedule(
                raw_tx["to"],
                raw_tx["value"],
                raw_tx["data"],
                predecessor.to_bytes(32, 'big'),
                salt.to_bytes(32, 'big'),
                delay
            )
        elif length > 1:
            targets = split_by(raw_transactions, "to")
            values = split_by(raw_transactions, "value")
            datas = split_by(raw_transactions, "data")
            schedule_tx = self.time_lock_controller.scheduleBatch(
                targets,
                values,
                datas,
                predecessor.to_bytes(32, 'big'),
                salt.to_bytes(32, 'big'),
                delay
            )
        return schedule_tx

    def execute_tx(
            self, raw_transactions: List[dict], length: int, predecessor: int = 0, salt: int = 0
    ):
        execute_tx = None
        if length == 1:
            raw_tx = raw_transactions[0]
            execute_tx = self.time_lock_controller.execute(
                raw_tx["to"],
                raw_tx["value"],
                raw_tx["data"],
                predecessor.to_bytes(32, 'big'),
                salt.to_bytes(32, 'big'),
            )
        elif length > 1:
            targets = split_by(raw_transactions, "to")
            values = split_by(raw_transactions, "value")
            datas = split_by(raw_transactions, "data")
            execute_tx = self.time_lock_controller.executeBatch(
                targets,
                values,
                datas,
                predecessor.to_bytes(32, 'big'),
                salt.to_bytes(32, 'big'),
            )
        return execute_tx
