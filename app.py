from blockchain import blockchain
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

# "python -m flask --app app.py run" or "flask run"--> CMD to run a server

app = Flask(__name__)
app.secret_key = "admin"

# Konfiguracja bazy danych PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123qweasd@localhost/hospital'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

#Definiowanie modeli ktore beda odpowiadac tabelkom z bazy danych
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Klucz główny
    login = db.Column(db.String(40))
    password = db.Column(db.String(200))
    patients = db.relationship('Patient', backref='user', lazy=True)  # Relacja z tabelą patients

class Patient(db.Model):
    __tablename__ = 'patients'
    block_id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Klucz obcy odwołujący się do users

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