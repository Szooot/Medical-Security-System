import hashlib
import datetime
import json
from flask import Flask, jsonify, render_template, request, redirect, url_for

class  Blockchain:
# Konstruktor
    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, previousHash = "0", patientData="Genesis Block")

# Tworzenie nowego bloku (pacjenta)
    def createBlock(self, proof, previousHash, patientData):
        block = {"index": len(self.chain) + 1,
                 "timestamp": str(datetime.datetime.now()),
                 "proof": proof,
                 "previous_hash": previousHash,
                 "data":patientData}
        block_string = json.dumps(block, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_string).hexdigest()
        block["hash"] = block_hash
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
            hash_operation = hashlib.sha256(str(new_proof**4 - previousProof**2).encode()).hexdigest()
            if hash_operation[0:4] == "0000":
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
            if hash_operation[0:4] != "0000":
                return False
            previousBlock = block
            blockIndex += 1
        return True
    
# Instancja klasy
blockchain = Blockchain()

# "python -m flask --app blockchain.py run" --> CMD to run a server

# Renderujemy pliki HTML po wejsciu na endpoint'y
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/patient_form")
def patientData():
    return render_template("patient_form.html")

# Wydobywamy nowy blok(dodawanie nowego pacjenta)
@app.route("/mine_block", methods = ["GET", "POST"])
def mine_block():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        pesel = request.form["pesel"]
        disease = request.form["disease"]
        patientData = {
            "name": name,
            "surname": surname,
            "pesel": pesel,
            "disease": disease }
    previousBlock = blockchain.getPrevBlock()
    previousProof = previousBlock["proof"]
    proof = blockchain.proof_of_work(previousProof)
    previousHash = blockchain.chain[-1]["hash"]
    blockchain.createBlock(proof, previousHash, patientData)
    return redirect(url_for("index"))

# Sprawdzamy caly blockchain
@app.route("/get_chain", methods = ["GET"])
def get_chain():
    response = {
        "chain": [
            {
                "index": block["index"],
                "timestamp": block["timestamp"],
                "proof": block["proof"],
                "hash": block["hash"],
                "previous_hash": block["previous_hash"]
            }
            for block in blockchain.chain
        ],
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200

# Sprawdzamy konkretny blok(pacjenta)
@app.route("/get_block", methods = ["GET", "POST"])
def get_block():
    if request.method == "POST":
        number = int(request.form["block_number"])
        pesel = request.form["block_pesel"]
    if number > len(blockchain.chain) and number < 1:
        return jsonify({"error": "Invalid block number. Block number exceeds the length of the blockchain."}), 400
    else:
        if pesel != blockchain.chain[number-1]["data"]["pesel"]:
            return jsonify({"error": "Invalid block number. Block number exceeds the length of the blockchain."}), 400
        else:
            response = blockchain.chain[number-1]
            return jsonify(response), 200
    
## Sprawdzay czy skrypt jest uruchamiany bezposrednio z glownego modulu
if __name__ == "__main__":
    app.run(debug=True)