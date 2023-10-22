from db import db
import users, topics
from sqlalchemy.sql import text


def get_list():
    sql = text("SELECT id, conversation FROM conversations")
    result = db.session.execute(sql)
    return result.fetchall()

def get_id(name):
    sql = text("SELECT id FROM conversations WHERE conversation=:name")
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()

def get_name(id):
    sql = text("SELECT conversation FROM conversations WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_user_conversations(user_id):
    sql = text("SELECT C.id, C.conversation FROM conversations C, users U WHERE C.user_id=U.id AND C.user_id=:user_id ORDER BY C.id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def create_conversation(convo, topic_id):
    tpcs = topics.get_list()
    if topic_id not in tpcs == True:
        return False
    user_id = users.user_id()
    if user_id == 0:
        return False
    else:
        sql = text("INSERT INTO conversations (conversation, user_id, created_at, topic_id) VALUES (:convo, :user_id, NOW(), :topic_id)")
        db.session.execute(sql, {"convo":convo, "user_id":user_id, "topic_id":topic_id})
        db.session.commit()
    return True

def alter_converstaion(new_convo, convo_id):
    sql = text("UPDATE conversations SET conversation=:new_convo WHERE id=:convo_id")
    db.session.execute(sql, {"new_convo":new_convo, "convo_id":convo_id})
    db.session.commit()

    return True

def delete_conversation(convo_id):
    sql =  text("DELETE FROM messages WHERE convo_id IN (:convo_id)")
    db.session.execute(sql, {"convo_id":convo_id})

    sql =  text("DELETE FROM conversations WHERE id=:id")
    db.session.execute(sql, {"id":convo_id})

    db.session.commit()