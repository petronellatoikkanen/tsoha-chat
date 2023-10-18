from db import db
import users, conversations
from sqlalchemy.sql import text

def get_list(convo_name):
    sql = text("SELECT M.sent_at, M.content, U.username FROM messages M, users U, conversations C WHERE M.user_id=U.id AND M.convo_name=:convo_name AND C.visible=1 and M.visible=1 GROUP BY M.id,M.sent_at, M.content, U.username  ORDER BY M.id")
    result = db.session.execute(sql, {"convo_name": convo_name})
    return result.fetchall()

def get_user_messages(user_id):
    sql = text("SELECT M.id, M.sent_at, M.content, U.username, m.convo_name FROM messages M, users U, conversations C WHERE M.user_id=U.id AND m.user_id=:user_id AND m.visible=1 GROUP BY m.convo_name, M.id,M.sent_at, M.content, U.username  ORDER BY M.convo_name")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def send_message(content, convo):
    convos = conversations.get_list()
    if convo not in convos == True:
        return False
    user_id = users.user_id()
    if user_id == 0:
        return False
    else:
        sql = text("INSERT INTO messages (content, user_id, sent_at, convo_name) VALUES (:content, :user_id, NOW(), :convo)")
        db.session.execute(sql, {"content":content, "user_id":user_id, "convo":convo})
        db.session.commit()
    return True


def search_message(word):
    sql = text("SELECT M.sent_at, M.content, U.username, M.convo_name FROM messages M, users U, conversations C WHERE M.user_id=U.id AND m.visible=1 AND c.visible=1 AND LOWER(content) LIKE LOWER(:word)")
    result = db.session.execute(sql, {"word": '%'+ word + '%'})
    return result.fetchall()


def alter_message(message, message_id):
    sql = text("UPDATE messages SET content=:message WHERE id=:message_id")
    db.session.execute(sql, {"message":message, "message_id":message_id})
    db.session.commit()
    return True

def delete_message(message_id):
    sql =  text("UPDATE messages SET visible=0 WHERE id=:id")
    db.session.execute(sql, {"id":message_id})
    db.session.commit()