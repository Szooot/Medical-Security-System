import hashlib
import datetime
import json
from flask import Flask

# python -m flask --app blockchain.py run --> CMD to run server
app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<h1>xd</h1>"


class  Blockchain:

    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, previousHash = '0')
    
    def createBlock(self, proof, previousHash):
        block = {"index": len(self.chain) + 1,
                 "timestamp": str(datetime.datetime.now()),
                 "proof": proof,
                 "previous_hash": previousHash}
        self.chain.append(block)
        return block

    def getPrevBlock(self):
        return self.chain[-1]
    
    def proof_of_work(self, previousProof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previousProof**2).encode()).hexdigest()
            if hash_operation[0:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block["previous_hash"] != self.hash(previousBlock):
                return False
            previousProof = previousBlock["proof"]
            proof = block["proof"]    
            hash_operation = hashlib.sha256(str(proof**2 - previousProof**2).encode()).hexdigest()
            if hash_operation[0:4] != '0000':
                return False
            previousBlock = block
            blockIndex += 1
        return True
    

blockchain = Blockchain()
print(blockchain.chain[0]["index"])


