import hashlib
import datetime
import json
from config import db  # Zamiast importu z app.py

class Blockchain:
    # Konstruktor
    def __init__(self):
        self.chain = []
        self.createBlock(proof=1, previousHash="0", patientData="Genesis Block")

    # Tworzenie nowego bloku (pacjenta)
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

    # Sprawdzenie ostatniego bloku
    def getPrevBlock(self):
        return self.chain[-1]

    # Dowód pracy wydobycia bloku
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

    # Funkcja haszująca
    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()

    # Sprawdzenie czy łańcuch jest poprawny
    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block["previous_hash"] != self.hash(previousBlock):
                return False
            previousProof = previousBlock["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(str(proof ** 2 - previousProof ** 2).encode()).hexdigest()
            if hash_operation[0:4] != "0000":
                return False
            previousBlock = block
            blockIndex += 1
        return True

# Instancja klasy
blockchain = Blockchain()