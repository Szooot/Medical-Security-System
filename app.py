from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import app, db
from blockchain import blockchain
import json

# Data hash fucntion before adding to database
def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

# Database table models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40))
    password = db.Column(db.String(200))

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

# Generate Genesis Block if it's not exist
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

# Endpoint for checking if user is logged in
@app.route('/is_logged_in') 
def is_logged_in():
    logged_in = 'username' in session
    return jsonify(logged_in=logged_in)

# Endpoint for logout
@app.route('/logout') 
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# Login endpoint
@app.route('/login', methods=['POST', 'GET'])  
def login():
    username = request.form.get('username')
    raw_password = request.form.get('password')
     # Checking for user in dataabse
    user = User.query.filter_by(login=username).first()
    # Checking if user exist and is password correct
    if user and check_password_hash(user.password, raw_password):
        session['username'] = username
        flash('Logged in successfully!', 'success')
        return redirect(url_for('index'))
    else:
        # If user or password incorrect, then flash error
        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('new_username')
    raw_password = request.form.get('new_password')
    password = hash_password(raw_password)
    # Creating new user and adding him to database
    new_user = User(login=username, password=password)
    # Adding user into session
    db.session.add(new_user)
    db.session.commit()
    session['username'] = username
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/patient_form")
def patientData():
    return render_template("patient_form.html")

# Adding new patient to the blockchain
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
        
        # Adding new block into database
        block_record = Block(
            index=new_index,
            timestamp=new_block["timestamp"],
            proof=new_block["proof"],
            hash=new_block["hash"],
            previous_hash=new_block["previous_hash"],
            user_id=user.id,
            patient_data=json.dumps(patientData)
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

# Checking all blocks of acctual logged user
@app.route("/get_block", methods = ["GET"])
def get_block():
    if 'username' not in session:
        flash('You need to be logged in to view your blocks', 'error')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(login=session['username']).first()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))

    user_blocks = Block.query.filter_by(user_id=user.id).all()
    blocks_data = [{
        "index": block.index,
        "timestamp": block.timestamp,
        "proof": block.proof,
        "hash": block.hash,
        "previous_hash": block.previous_hash,
        "data": json.loads(block.patient_data)
    } for block in user_blocks]

    return render_template('block.html', blocks_data=blocks_data)
    
# Checking if script is launched directly from main module
if __name__ == "__main__":
    app.run(debug=True)