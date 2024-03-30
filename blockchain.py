import hashlib
import datetime
import json
from flask import Flask, jsonify, render_template

class  Blockchain:

# Konstruktor
    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, previousHash = '0')

# Tworzenie nowego bloku (pacjenta)
    def createBlock(self, proof, previousHash, patientData = {"name":None}):
        block = {"index": len(self.chain) + 1,
                 "timestamp": str(datetime.datetime.now()),
                 "proof": proof,
                 "previous_hash": previousHash,
                 "data":patientData}
        self.chain.append(block)
        return block

# Sprawdzenie ostatniego bloku
    def getPrevBlock(self):
        return self.chain[-1]

# Dowod pracy wydobycia bloku
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

# Funkcja haszujaca
    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()

 # Sprawdzenie czy lancuch jest poprawny  
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
    
# Instancja klasy
blockchain = Blockchain()

# "python -m flask --app blockchain.py run" --> CMD to run a server

# Renderujemy plik HTML po wejsciu na root "/"
app = Flask(__name__, template_folder="src")
@app.route("/")
def index():
    return render_template("index.html")

# Wydobywamy nowy blok
@app.route("/mine_block", methods = ["GET"])
def mine_block():
    previousBlock = blockchain.getPrevBlock()
    previousProof = previousBlock["proof"]
    proof = blockchain.proof_of_work(previousProof)
    previousHash = blockchain.hash(previousBlock)
    block = blockchain.createBlock(proof, previousHash)
    response = {"message":"You've mined a block",
                "index":block["index"],
                "timestamp":block["timestamp"],
                "proof":block["proof"],
                "previous_hash":block["previous_hash"]}
    return jsonify(response), 200

# Sprawdzamy caly blockchain
@app.route("/get_chain", methods = ["GET"])
def get_chain():
    response = {"chain":blockchain.chain,
                "length":len(blockchain.chain)}
    return jsonify(response), 200

## Sprawdzay czy skrypt jest uruchamiany bezposrednio z glownego modulu
if __name__ == '__main__':
    app.debug = True
    app.run()