from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import app, db  # Importujemy app i db z config.py
from blockchain import blockchain  # Importujemy blockchain po zdefiniowaniu app i db
import json

def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

# Definiowanie modeli
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40))
    password = db.Column(db.String(200))
    patients = db.relationship('Patient', backref='user', lazy=True)

class Patient(db.Model):
    __tablename__ = 'patients'
    block_id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Block(db.Model):
    __tablename__ = 'blocks'
    index = db.Column(db.Integer, primary_key=True, nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    proof = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.String, nullable=False)
    previous_hash = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='blocks')
    patient_data = db.Column(db.Text)

# Funkcja inicjalizująca tabelę z Genesis Block
def initialize_genesis_block():
    genesis_block_exists = Block.query.filter_by(index=1).first() is not None
    if not genesis_block_exists:
        genesis_block = Block(
            index=1,
            timestamp=str(datetime.now()),
            proof=1,
            hash='0',
            previous_hash='0'
        )
        db.session.add(genesis_block)
        db.session.commit()
        print("Genesis Block initialized")
    else:
        print("Genesis Block already exists")

@app.before_request
def setup():
    db.create_all()
    initialize_genesis_block()

@app.route('/is_logged_in') #Endpoint for checking if user is logged in
def is_logged_in():
    logged_in = 'username' in session
    return jsonify(logged_in=logged_in)

@app.route('/logout') #Endpoint for logout
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST', 'GET'])  # Endpoint, który odbiera dane z formularza
def login():
    username = request.form.get('username')
    raw_password = request.form.get('password')
     # Pobranie użytkownika z bazy danych na podstawie nazwy użytkownika
    user = User.query.filter_by(login=username).first()
    
    # Sprawdzenie czy użytkownik istnieje i czy hasło jest poprawne
    if user and check_password_hash(user.password, raw_password):
        # Jeśli hasło jest poprawne, zapisz nazwę użytkownika w sesji
        session['username'] = username
        flash('Logged in successfully!', 'success')
        return redirect(url_for('index'))
    else:
        # Jeśli użytkownik nie istnieje lub hasło jest niepoprawne, wyświetl błąd
        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('index'))  # Możesz przekierować gdziekolwiek chcesz

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('new_username')
    raw_password = request.form.get('new_password')
    password = hash_password(raw_password)
    # Utworzenie nowego użytkownika i zapisanie go do bazy danych
    new_user = User(login=username, password=password)
    db.session.add(new_user)  # Dodaje do sesji
    db.session.commit()  # Zapisuje zmiany
    session['username'] = username
    return redirect(url_for('index'))  # Przekierowuje po zakończeniu operacji

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
@app.route("/mine_block", methods=["GET", "POST"])
def mine_block():
    if 'username' not in session:
        flash('You need to be logged in to mine a block', 'error')
        return redirect(url_for('login'))
    
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
        
        user = User.query.filter_by(login=session['username']).first()
        
        # Pobranie ostatniego bloku z bazy danych
        last_block = Block.query.order_by(Block.index.desc()).first()
        
        if last_block:
            previous_proof = last_block.proof
            previous_hash = last_block.hash
            new_index = last_block.index + 1
        else:
            previous_proof = 1  # Genesis Block proof
            previous_hash = '0'  # Genesis Block hash
            new_index = 1

        proof = blockchain.proof_of_work(previous_proof)
        new_block = blockchain.createBlock(proof, previous_hash, patientData)
        
        # Zapis nowego bloku do bazy danych
        block_record = Block(
            index=new_index,
            timestamp=new_block["timestamp"],
            proof=new_block["proof"],
            hash=new_block["hash"],
            previous_hash=new_block["previous_hash"],
            user_id=user.id,
            patient_data=json.dumps(patientData)  # Zapis danych pacjenta jako JSON
        )
        db.session.add(block_record)
        db.session.commit()
        
        flash("New patient added!")
        return redirect(url_for("index"))

@app.route("/get_chain", methods=["GET"])
def get_chain():
    chain_data = [{
            "index": block.index,
            "timestamp": block.timestamp,
            "proof": block.proof,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        }
        for block in Block.query.order_by(Block.index).all()
    ]
    chain_length = len(chain_data)
    return render_template("get_chain.html", chain=chain_data, length=chain_length)

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