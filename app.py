from flask import Flask, jsonify, request, session
import ast
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)


app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL = 'mysql+pymysql://root:erioluwa@localhost/onikolo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some_random_key'


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    banks = db.Column(db.Text)


class store_amount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    amount = db.Column(db.Text)

db. create_all()


@app.route("/signup", methods=["POST"])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")
    banks = request.json.get("banks")    
    new_user = user(username=username, password=password, banks=banks)
    db.session.add(new_user)
    thebank = ast.literal_eval(banks)
    print(thebank)
    amount = []
    for banks in thebank:
        amount.append(200000)
    print(amount)
    new_user_amount = store_amount(username=username,amount=str(amount))
    db.session.add(new_user) 
    db.session.add(new_user_amount)
    db.session.commit()
    return jsonify({
        "message" : "signup successful"
    })

@app.route("/login", methods=["POST"])
def login ():
    username = request.json.get('username')
    password = request.json.get('password')
    existing_user = user.query.filter_by(username=username, password=password).first()
    if not existing_user:
        return (jsonify({"message":"incorect username or password"})), 404
    session['username'] = username
    banks = existing_user.banks
    the_user_amount = store_amount.query.filter_by(username=username).first()
    the_amount = the_user_amount.amount
    print (the_amount)
    return (jsonify({
        "message": "login successful",
        "banks" : banks,
        "amount": the_amount
    })), 200

@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username')
        log_out = 'You have successfully logged out.'
        return (jsonify({"message": log_out}))
    return (jsonify({"message": "not logged in"}))

@app.route("/make_payment", methods=["POST"])
def make_payment():
    the_user = session.get("username")
    username = the_user
    payment = request.json.get('payment')
    if the_user:
        the_user = user.query.filter_by(username=username).first()
        the_banks = ast.literal_eval(the_user.banks)
        if "Standard Charts" in the_banks:
            charges = (1/100) * float(payment) 
            reward = (6/100) * float(payment)
            if reward > 10000:
                reward = 10000
                total_amount = float(payment) - float (charges) + float(reward)
                message = "we recomend you make use of Standard Charts you transferring " + str(payment) + " would result in N" + str(total_amount)
                return (jsonify({"message":message}))
            total_amount = float(payment) - float (charges) + float(reward)
            message = "we recomend you make use of Standard Charts you transferring " + str(payment) + " would result in N" + str(total_amount)
            return (jsonify({"message":message}))
        elif payment > 86957:
            if "Glory Trust Bank" in the_banks:
                charges = 70 
                reward = (5.75/100) * float(payment)
                if reward > 5000:
                    reward = 5000
                    total_amount = float(payment) - float (charges) + float(reward)
                    message = "we recomend you make use of Glory trust bank, you transferring " + str(payment) + " would result in N" + str(total_amount)
                total_amount = float(payment) - float (charges) + float(reward)
                message = "we recomend you make use of Glory trust bank, you transferring " + str(payment) + " would result in N" + str(total_amount)
        else:
            charges = 120
            reward = (6/100) * float(payment)
            if reward > 7000:
                reward = 7000
                total_amount = float(payment) - float (charges) + float(reward)
                message = "we recomend you make use of Glory trust bank, you transferring " + str(payment) + " would result in N" + str(total_amount)
            total_amount = float(payment) - float (charges) + float(reward)
            message = "we recomend you make use of Glory trust bank, you transferring " + str(payment) + " would result in N" + str(total_amount)
    return (jsonify({"message": "not logged in"}))

if "__main__" == __name__:
    app.run(debug=True)