from db import db
import users, topics
from sqlalchemy.sql import text


def get_list():
    sql = text("SELECT C.id, C.convo FROM conversations C, topics T Where T.visible=1 AND c.visible=1 group by c.id")
    result = db.session.execute(sql)
    return result.fetchall()

def get_user_conversations(user_id):
    sql = text("SELECT C.id, C.convo FROM conversations C, users U WHERE C.user_id=U.id AND C.user_id=:user_id AND c.visible=1 ORDER BY C.convo")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def create_conversation(convo, topic):
    tpcs = topics.get_list()
    if topic not in tpcs == True:
        return False
    user_id = users.user_id()
    if user_id == 0:
        return False
    else:
        sql = text("INSERT INTO conversations (convo, user_id, created_at, topic_name) VALUES (:convo, :user_id, NOW(), :topic)")
        db.session.execute(sql, {"convo":convo, "user_id":user_id, "topic":topic})
        db.session.commit()
    return True

def alter_converstaion(new_convo, convo_id):
    sql = text("UPDATE conversations SET convo=:new_convo WHERE id=:convo_id")
    db.session.execute(sql, {"convo":convo, "convo_id":convo_id})
    db.session.commit()
    return True

def delete_conversation(convo_id):
    sql =  text("UPDATE conversations SET visible=0 WHERE id=:id")
    db.session.execute(sql, {"id":convo_id})
    db.session.commit()