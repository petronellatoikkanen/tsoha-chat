from db import db
import users, topics
from sqlalchemy.sql import text


def get_list():
    sql = text("SELECT C.id, C.convo FROM conversations C, topics T Where T.visible=1 group by c.id")
    result = db.session.execute(sql)
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

