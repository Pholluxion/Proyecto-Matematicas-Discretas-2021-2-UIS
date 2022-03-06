from distutils.log import error
from black import err
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from encryptor import Encryptor
from sqlite3 import Error
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "secret"
app.config["SESSION_TYPE"] = "filesystem"

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

listUsers = []

class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    private_key = db.Column(db.String, unique=True, nullable=False)
    public_key = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


Session(app)

socketio = SocketIO(app, manage_session=False)

db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():

    if request.method == "POST":

        username = request.form["username"]
        room = request.form["room"]

        encryptor = Encryptor()

        encryptor.username = username
        
        userDB = User.query.filter_by(username=username).first()

        if(userDB):

            session["username"] = userDB.username
            session["room"] = room
            session["private_key"] = userDB.private_key
            session["public_key"] = userDB.public_key

        else:
            
            session["username"] = username
            session["room"] = room
            session["private_key"] = encryptor.getPrivateKey()
            session["public_key"] = encryptor.getPublicKey()


            try:
                user = User(username = username,private_key = encryptor.getPrivateKey(),public_key=encryptor.getPublicKey())
                db.session.add(user)

            except(error):

                print(error)
                
            db.session.commit()

        return render_template("chat.html", session=session)
    else:
        if session.get("username") is not None:
            return render_template("chat.html", session=session)
        else:
            return redirect(url_for("index"))


@socketio.on("join", namespace="/chat")
def join(message):
    room = session.get("room")
    join_room(room)
    emit("status", {"msg": session.get("username")}, room=room)


@socketio.on("text", namespace="/chat")
def text(message):
    room = session.get("room")
    emit(
        "message", {"msg": session.get("username") + " : " + message["msg"]}, room=room
    )


@socketio.on("left", namespace="/chat")
def left(message):
    room = session.get("room")
    username = session.get("username")
    leave_room(room)
    session.clear()
    emit("status", {"msg": username + " salió"}, room=room)


if __name__ == "__main__":
    socketio.run(app)
