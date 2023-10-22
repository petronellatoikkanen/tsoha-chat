from db import db
import users, conversations
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT id, message FROM Messages")
    result = db.session.execute(sql)
    return result.fetchall()

def get_list_by_conversation(convo_id):
    sql = text("SELECT M.sent_at, M.message, U.username FROM messages M, users U, conversations C WHERE M.user_id=U.id AND M.convo_id=C.id AND M.convo_id=:convo_id  GROUP BY M.id, M.sent_at, M.message, U.username ORDER BY M.sent_at DESC")
    result = db.session.execute(sql, {"convo_id": convo_id})
    return result.fetchall()

def get_user_messages(user_id):
    sql = text("SELECT M.id, M.message, C.conversation FROM messages M LEFT JOIN conversations C ON M.convo_id=C.id WHERE m.user_id=:user_id GROUP BY M.id, C.conversation ORDER BY M.convo_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def send_message(message, convo):
    convos = conversations.get_list()
    if convo not in convos == True:
        return False
    user_id = users.user_id()
    if user_id == 0:
        return False
    else:
        convo_id = conversations.get_id(convo)[0]

        sql = text("SELECT topic_id FROM conversations WHERE id=:convo_id")
        topic = db.session.execute(sql, {"convo_id":convo_id}).fetchone()
        topic_id = topic[0]

        sql = text("INSERT INTO messages (message, user_id, sent_at, convo_id, topic_id) VALUES (:message, :user_id, NOW(), :convo_id, :topic_id)")
        db.session.execute(sql, {"message":message, "user_id":user_id, "convo_id":convo_id, "topic_id":topic_id})
        db.session.commit()
    return True



def search_message(word):
    sql = text("SELECT M.sent_at, M.message, U.username, C.conversation FROM messages M, users U, conversations C WHERE M.user_id=U.id AND LOWER(message) LIKE LOWER(:word)")
    result = db.session.execute(sql, {"word": '%'+ word + '%'})
    return result.fetchall()


def alter_message(message, message_id):
    sql = text("UPDATE messages SET message=:message WHERE id=:message_id")
    db.session.execute(sql, {"message":message, "message_id":message_id})
    db.session.commit()
    return True

def delete_message(message_id):
    sql =  text("DELETE FROM messages WHERE id=:id")
    db.session.execute(sql, {"id":message_id})
    db.session.commit()