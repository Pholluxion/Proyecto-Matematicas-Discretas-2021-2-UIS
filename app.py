from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from encryptor import Encryptor


app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "secret"
app.config["SESSION_TYPE"] = "filesystem"



listUsers = []


Session(app)

socketio = SocketIO(app, manage_session=False)


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

        session["username"] = username
        session["room"] = room
        session["private_key"] = encryptor.getPrivateKey()
        session["public_key"] = encryptor.getPublicKey()


        listUsers.append(encryptor)
        print(listUsers)

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

    for user in listUsers:

        print(user.username)

        if user.username == session.get("username"):

            messageE = user.encryptMessage(message["msg"])

            messageD = user.decryptMessage(messageE)

            emit(
                "message",
                {"msg": session.get("username") + " : " + str(messageD)},
                room=room,
            )

            emit(
                "messageE",
                {"msg": session.get("username") + " : " + str(messageE)},
                room=room,
            )



@socketio.on("left", namespace="/chat")
def left(message):
    room = session.get("room")
    username = session.get("username")
    leave_room(room)
    session.clear()
    emit("status", {"msg": username + " sali??"}, room=room)


if __name__ == "__main__":
    socketio.run(app)
