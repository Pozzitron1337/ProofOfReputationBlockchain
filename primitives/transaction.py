from eth_account import Account 
import hashlib
import json

class Transaction:

    def __init__(self, data):
        self.data = data
        self.signatures: list() = []

    def __repr__(self) -> str:
        transactionInfo = {
            'data':self.data,
            'signatures':self.signatures
        }
        return json.dumps(transactionInfo)
    
    def getData(self):
        dataInfo = {
            'data':self.data
        }
        return json.dumps(dataInfo)
    
    def getDataHash(self):
        transactionData = self.getData().encode()
        transactionHash = "0x" + hashlib.sha3_256(transactionData).hexdigest()
        return transactionHash
    
    def sign(self, privateKey):
        transactionDataHash = self.getDataHash()
        signData = Account.signHash(transactionDataHash, privateKey)
        self.signatures.append(signData.signature.hex())

    def getSigners(self):
        transactionDataHash = self.getDataHash()
        signers = []
        for signature in self.signatures:
            signer = Account.recoverHash(message_hash=transactionDataHash, signature=signature)
            signers.append(signer)
        signersInfo = {
            'signers':signers
        }
        return json.dumps(signersInfo)

    

   
    