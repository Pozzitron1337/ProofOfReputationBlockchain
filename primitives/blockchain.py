
from .block import Block

class Blockchain:

    def __init__(self) -> None:
        self.blockchain: list(Block) = []

    def setBlockchain(self, blockchain: list()):
        self.blockchain = blockchain

    def addBlock(self, block: Block) -> None:
        self.blockchain.append(block)

    def getBlock(self, blockNumber) -> Block:
        blockchainLength = self.getBlockchainLength()
        if blockNumber > blockchainLength:
            blockNumber = blockchainLength - 1
        return self.blockchain[blockNumber]

    def getLastBlock(self) -> Block:
        return self.blockchain[-1]

    def getBlockchainLength(self) -> int:
        return len(self.blockchain)
    
    def getBlockchainList(self) -> list():
        return self.blockchain
    
    



# b0 = Block(0, "leader0")
# b1 = Block(1, "leader1")
# blockchain = Blockchain()

# blockchain.addBlock(b0)

# print(blockchain.getBlockchainLength())

# blockchain.addBlock(b1)

# print(blockchain.getBlockchainLength())

# print(blockchain.getBlockchainList())

# print(b1.getHash())

