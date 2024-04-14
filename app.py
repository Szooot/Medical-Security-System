from blockchain import blockchain
from flask import Flask, render_template, request, redirect, url_for, flash, session
 
# "python -m flask --app app.py run" --> CMD to run a server

# Renderujemy pliki HTML po wejsciu na endpoint'y
app = Flask(__name__)
app.secret_key = "admin"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_block_form")
def index2():
    return render_template("get_block.html")

@app.route("/patient_form")
def patientData():
    return render_template("patient_form.html")

# Wydobywamy nowy blok(dodawanie nowego pacjenta)
@app.route("/mine_block", methods = ["GET", "POST"])
def mine_block():
    if request.method == "POST":
        name = request.form["name"].capitalize()
        surname = request.form["surname"].capitalize()
        age = request.form["age"]
        city = request.form["city"].capitalize()
        pesel = request.form["pesel"]
        disease = request.form["disease"].capitalize()
        patientData = {
            "name": name,
            "surname": surname,
            "age": age,
            "city": city,
            "pesel": pesel,
            "disease": disease  
        }
    previousBlock = blockchain.getPrevBlock()
    previousProof = previousBlock["proof"]
    proof = blockchain.proof_of_work(previousProof)
    previousHash = blockchain.chain[-1]["hash"]
    blockchain.createBlock(proof, previousHash, patientData)
    flash("New patient added!")
    return redirect(url_for("index"))

# Sprawdzamy caly blockchain
@app.route("/get_chain", methods = ["GET"])
def get_chain():
    chain_data = [{
            "index": block["index"],
            "timestamp": block["timestamp"],
            "proof": block["proof"],
            "hash": block["hash"],
            "previous_hash": block["previous_hash"]
        }
        for block in blockchain.chain
    ]
    chain_length = len(blockchain.chain)
    return render_template("get_chain.html", chain = chain_data, length = chain_length)

# Sprawdzamy konkretny blok(pacjenta)
@app.route("/get_block", methods = ["GET", "POST"])
def get_block():
    if request.method == "POST":
        number = int(request.form["block_number"])
        pesel = request.form["block_pesel"]
    if number == 1:
        response = {
                "index": blockchain.chain[number-1]["index"],
                "timestamp": blockchain.chain[number-1]["timestamp"],
                "proof": blockchain.chain[number-1]["proof"],
                "previous_hash": blockchain.chain[number-1]["previous_hash"],
                "data": blockchain.chain[number-1]["data"]
            }
        return render_template("block.html", block_data = response)
    if number > len(blockchain.chain) or number < 1:
        flash("Invalid block number")
        return redirect(url_for("index"))
    else:
        if pesel != blockchain.chain[number-1]["data"]["pesel"]:
            flash("Invalid pesel")
            return redirect(url_for("index"))
        else:
            response = {
                "index": blockchain.chain[number-1]["index"],
                "timestamp": blockchain.chain[number-1]["timestamp"],
                "proof": blockchain.chain[number-1]["proof"],
                "previous_hash": blockchain.chain[number-1]["previous_hash"],
                "data": blockchain.chain[number-1]["data"]
            }
            return render_template("block.html", block_data = response)
    
## Sprawdzay czy skrypt jest uruchamiany bezposrednio z glownego modulu
if __name__ == "__main__":
    app.run(debug=True)