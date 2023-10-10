from app import app
from flask import render_template, request, redirect
import messages, users, conversations, topics

@app.route("/")
def index():
    info = topics.indexinfo()
    convos = conversations.get_list()
    return render_template("index.html", info=info, convos=convos)


####################### messages  #########################

@app.route("/new_message")
def new_messages():
    convos = conversations.get_list()
    return render_template("new_message.html", convos=convos)

@app.route("/send_message", methods=["POST"])
def send_message():
    content = request.form["content"]
    convo = request.form["convo"]
    if messages.send_message(content, convo):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")


@app.route("/search_messages")
def seacrh_m():
   return render_template("search_messages.html")

@app.route("/search_message", methods=["POST"])
def search_message():
    word = request.form["word"]
    msgs = messages.search_message(word)
    return render_template("search_messages_result.html", word = word, msgs = msgs)



#######################  conversations #########################

@app.route("/new_conversation")
def new_conversations():
    tpcs = topics.get_list()
    return render_template("new_conversation.html", tpcs=tpcs)

@app.route("/create_conversation", methods=["POST"])
def create_conversation():
    topic = request.form["topic"]
    convo = request.form["convo"]
    if conversations.create_conversation(convo, topic):
        return redirect("/")
    else:
        return render_template("error.html", message="Keskustelun aloittaminen ei onnistunut, tarkista keskustelualueen nimi ja kokeile uudestaan")


####################### show conversation ####################


@app.route("/conversation/<convo_name>")
def show_conversation(convo_name):
    convo_name = convo_name
    msgs = messages.get_list(convo_name)

    return render_template("conversation.html", convo_name=convo_name, msgs=msgs)


####################### topics #########################


@app.route("/new_topic")
def new_topics():
    convos = conversations.get_list()
    return render_template("new_topic.html")


@app.route("/create_topic", methods=["POST"])
def create_topic():
    topic = request.form["topic"]
    if topics.create_topic(topic):
        return redirect("/")
    else:
        return render_template("error.html", message="Alueen luominen ei onnistut, yritä uudestaan")


@app.route("/remove", methods=["get", "post"])
def remove_topic():
    users.require_role(2)

    if request.method == "GET":
        tpcs = topics.get_list()
        return render_template("remove.html", tpcs=tpcs)

    if request.method == "POST":
        users.check_csrf()

        if "topic" in request.form:
            topic_id = request.form["topic"]
            topics.remove_topic(topic_id)

        return redirect("/")


########################## login, logout, register #########################

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

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Rekisteröinti ei onnistunut, tuntematon käyttäjärooli")

        if users.register(username, password1, role):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut, käyttäjätunnus käytössä")