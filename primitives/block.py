from .transaction import Transaction
import hashlib
import json

class Block: 

    def __init__(self, blockNumber = None, leader = "unknownLeader") -> None:
        self.blockNumber: int = blockNumber
        self.leader = leader
        self.transactions: list(Transaction) = []

    def __repr__(self) -> str:
        return self.toJSON()


    def toJSON(self) -> str:
        blockInfo = {
            'blockNumber':self.blockNumber,
            'leader':self.leader,
            'transactions':self.transactions
        }
        return json.dumps(blockInfo)

    def loadBlockFromJSON(self, block_json):
        blockInfo = json.loads(block_json)
        self.blockNumber = blockInfo['blockNumber']
        self.leader = blockInfo['leader']
        self.transactions = blockInfo['transactions']
        return self

    def setTransactions(self, transactions) -> None:
        self.transactions = transactions

    def addTransaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def getHash(self):
        blockInfo = self.toJSON().encode()
        blockHash = hashlib.sha3_256(blockInfo)
        return blockHash.hexdigest()
