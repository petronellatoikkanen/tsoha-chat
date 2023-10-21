from db import db
import users, conversations
from sqlalchemy.sql import text

def get_list(convo_name):
    sql = text("SELECT M.sent_at, M.message, U.username FROM messages M, users U, conversations C WHERE M.user_id=U.id AND M.convo_id=:C.id AND C.visible=1 and M.visible=1 GROUP BY M.id, M.sent_at, M.message, U.username ORDER BY M.id")
    result = db.session.execute(sql, {"convo_name": convo_name})
    return result.fetchall()

def get_user_messages(user_id):
    sql = text("SELECT M.id, M.sent_at, M.message, U.username, C.conversation FROM messages M, users U, conversations C WHERE M.user_id=U.id AND m.user_id=:user_id AND m.visible=1 GROUP BY M.message, m.convo_id, M.id, M.sent_at U.username ORDER BY M.convo_id")
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
        sql = text("INSERT INTO messages (message, user_id, sent_at, convo_id) VALUES (:message, :user_id, NOW(), :convo)")
        db.session.execute(sql, {"message":message, "user_id":user_id, "convo":convo})
        db.session.commit()
    return True


def search_message(word):
    sql = text("SELECT M.sent_at, M.message, U.username, C.conversation FROM messages M, users U, conversations C WHERE M.user_id=U.id AND m.visible=1 AND c.visible=1 AND LOWER(message) LIKE LOWER(:word)")
    result = db.session.execute(sql, {"word": '%'+ word + '%'})
    return result.fetchall()


def alter_message(message, message_id):
    sql = text("UPDATE messages SET message=:message WHERE id=:message_id")
    db.session.execute(sql, {"message":message, "message_id":message_id})
    db.session.commit()
    return True

def delete_message(message_id):
    sql =  text("UPDATE messages SET visible=0 WHERE id=:id")
    db.session.execute(sql, {"id":message_id})
    db.session.commit()