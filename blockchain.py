import hashlib
import datetime
import json
from config import db

class Blockchain:
    # Consturctor
    def __init__(self):
        self.chain = []
        self.createBlock(proof=1, previousHash="0", patientData="Genesis Block")

    # Creating new blcok
    def createBlock(self, proof, previousHash, patientData):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previousHash,
            "data": patientData
        }
        block_string = json.dumps(block, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_string).hexdigest()
        block["hash"] = block_hash
        self.chain.append(block)
        return block

    # Checking last block
    def getPrevBlock(self):
        return self.chain[-1]

    # Proof of Work
    def proof_of_work(self, previousProof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof ** 4 - previousProof ** 2).encode()).hexdigest()
            if hash_operation[0:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    # Hash function
    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()

# Blockchain instance
blockchain = Blockchain()