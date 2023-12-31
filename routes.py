from app import app
from flask import render_template, request, redirect
import users, messages, conversations, topics, secret_topics, secret_messages

@app.route("/")
def index():
    info = topics.indexinfo()
    convos = conversations.get_list()
    user_id = users.user_id()
    secret_t = secret_topics.index_list(user_id)
    return render_template("index.html", info=info, convos=convos, secret_t=secret_t)

@app.route("/conversations")
def show_conversations():
    info = topics.indexinfo()
    convos = conversations.get_list()
    user_id = users.user_id()
    secret_t = secret_topics.index_list(user_id)
    return render_template("conversations.html", info=info, convos=convos, secret_t=secret_t)


####################### messages  #########################
# # # new, send, delete
@app.route("/new_message/<convo_conversation>")
def new_messages(convo_conversation):
    convo_id = conversations.get_id(convo_conversation)
    msgs = messages.get_list_by_conversation(convo_id[0])

    return render_template("new_message.html", convo_conversation=convo_conversation, msgs=msgs)


@app.route("/send_message", methods=["POST"])
def send_message():
    content = request.form["content"]
    convo = request.form["convo"]
    if messages.send_message(content, convo):
        return show_conversation(convo)
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")


@app.route("/delete_message", methods=["get", "post"])
def delete_message():
    user_id = users.user_id()
    if request.method == "GET":
        msgs = messages.get_user_messages(user_id)
        return render_template("delete_message.html", msgs=msgs)

    if request.method == "POST":
        users.check_csrf()

        if "message" in request.form:
            message_id = request.form["message"]
            messages.delete_message(message_id)

        return redirect("/")

# # #search
@app.route("/search_messages")
def seacrh_m():
   return render_template("search_messages.html")

@app.route("/search_message", methods=["POST"])
def search_message():
    word = request.form["word"]
    msgs = messages.search_message(word)
    return render_template("search_messages_result.html", word = word, msgs = msgs)



#######################  conversations #########################
# # # new, send, delete
@app.route("/new_conversation")
def new_conversations():
    tpcs = topics.get_list()
    return render_template("new_conversation.html", tpcs=tpcs)

@app.route("/create_conversation", methods=["POST"])
def create_conversation():
    topic_id = request.form["topic_id"]
    convo = request.form["convo"]
    if conversations.create_conversation(convo, topic_id):
        return redirect("/")
    else:
        return render_template("error.html", message="Keskustelun aloittaminen ei onnistunut, tarkista keskustelualueen nimi ja kokeile uudestaan")

@app.route("/delete_conversation", methods=["get", "post"])
def delete_conversation():
    user_id = users.user_id()
    if request.method == "GET":
        convos = conversations.get_user_conversations(user_id)
        return render_template("delete_conversation.html", convos=convos)

    if request.method == "POST":
        users.check_csrf()

        if "convo" in request.form:
            convo_id = request.form["convo"]
            conversations.delete_conversation(convo_id)

        return redirect("/")

# # # view
@app.route("/conversation/<convo_conversation>")
def show_conversation(convo_conversation):
    convo_id = conversations.get_id(convo_conversation)
    msgs = messages.get_list_by_conversation(convo_id[0])

    return render_template("conversation.html", convo_conversation=convo_conversation, msgs=msgs)


####################### topics #########################
# # # create and delete

@app.route("/new_topic")
def new_topics():
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


####################### secret topics #########################
# # # create and delete

@app.route("/new_secret_topic")
def new_secret_topics():
    users_list = users.get_list()
    return render_template("new_secret_topic.html", users_list=users_list)


@app.route("/create_secret_topic", methods=["POST"])
def create_secret_topic():
    secret_topic = request.form["secret_topic"]
    users_list = request.form.getlist("users_list[]")
    if secret_topics.create_secret_topic(secret_topic):
        secret_topic_id = secret_topics.get_secret_topic_id(secret_topic)
        for user_id in users_list:
            secret_topics.add_secret_topic_user(secret_topic_id[0], user_id)
        return redirect("/")
    
    else:
        return render_template("error.html", message="Alueen luominen ei onnistut, yritä uudestaan")


@app.route("/remove_secret_topic", methods=["get", "post"])
def remove_secret_topic():
    users.require_role(2)

    if request.method == "GET":
        tpcs = secret_topics.get_list()
        return render_template("remove_secret_topic.html", tpcs=tpcs)

    if request.method == "POST":
        users.check_csrf()

        if "secret_topic" in request.form:
            secret_topic_id = request.form["secret_topic"]
            secret_topics.remove_secret_topic(secret_topic_id)

        return redirect("/")


# # # view
@app.route("/secret_topic/<secret_topic>")
def show_secret_topic(secret_topic):
    secret_topic_id = secret_topics.get_secret_topic_id(secret_topic)
    msgs = secret_messages.get_list_by_topic(secret_topic_id[0])

    return render_template("secret_topic.html", secret_topic=secret_topic, msgs=msgs)


####################### secret messages  #########################
# # # new, send, delete
@app.route("/new_secret_message/<secret_topic>")
def new_secret_messages(secret_topic):
    secret_topic_id = secret_topics.get_secret_topic_id(secret_topic)
    msgs = secret_messages.get_list_by_topic(secret_topic_id[0])

    return render_template("new_secret_message.html", secret_topic=secret_topic, msgs=msgs)


@app.route("/send_secret_message", methods=["POST"])
def send_secret_message():
    content = request.form["content"]
    secret_topic = request.form["secret_topic"]
    if secret_messages.send_secret_message(content, secret_topic):
        return show_secret_topic(secret_topic)
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")


@app.route("/delete_secret_message", methods=["get", "post"])
def delete_secret_message():
    user_id = users.user_id()
    if request.method == "GET":
        msgs = secret_messages.get_user_messages(user_id)
        return render_template("delete_secret_message.html", msgs=msgs)

    if request.method == "POST":
        users.check_csrf()

        if "secret_message" in request.form:
            secret_message_id = request.form["secret_message"]
            secret_messages.delete_secret_message(secret_message_id)

        return show_conversations()



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