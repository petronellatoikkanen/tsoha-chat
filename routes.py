from app import app
from flask import render_template, request, redirect
import messages, users, conversations, topics

@app.route("/")
def index():
    msgs = messages.get_list()
    convos = conversations.get_list()
    tpcs = topics.get_list()
    return render_template("index.html", countt=len(tpcs), countc=len(convos), countm=len(msgs), conversations=convos, messages=msgs, topics=tpcs)

@app.route("/new_message")
def new_messages():
    return render_template("new_message.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    content = request.form["content"]
    if messages.send_message(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")


@app.route("/new_conversation")
def new_conversations():
    return render_template("new_conversation.html")

@app.route("/create_conversation", methods=["POST"])
def create_conversation():
    convo = request.form["convo"]
    if conversations.create_conversation(convo):
        return redirect("/")
    else:
        return render_template("error.html", message="Keskustelun aloittaminen ei onnistunut")


@app.route("/new_topic")
def new_topics():
    return render_template("new_topic.html")

@app.route("/create_topic", methods=["POST"])
def create_topic():
    topic = request.form["topic"]
    if topics.create_topic(topic):
        return redirect("/")
    else:
        return render_template("error.html", message="Alueen luominen ei onnistu, pyydä ylläpitäjää luomaan alue")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Rekisteröinti ei onnistunut, salasanat eivät vastaa toisiaan")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut, käyttäjätunnus käytössä")