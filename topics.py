from db import db
import users
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT id, topic FROM topics ")
    result = db.session.execute(sql)
    return result.fetchall()

def indexinfo():
    sql = text("SELECT T.topic, COALESCE(count(distinct(C.conversation)), 0), COALESCE(count(M.message), 0), COALESCE(NULLIF(MAX(M.sent_at), NULL), NULL) FROM topics T LEFT JOIN conversations C on T.id=C.topic_id LEFT JOIN messages M on C.id=M.convo_id group by T.id")
    result = db.session.execute(sql)
    return result.fetchall()

def create_topic(topic):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO topics (topic, user_id, created_at) VALUES (:topic, :user_id, NOW())")
    
    try:
        db.session.execute(sql, {"topic":topic, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False


def remove_topic(topic_id):
    sql =  text("DELETE FROM messages WHERE topic_id IN (:topic_id)")
    db.session.execute(sql, {"topic_id":topic_id})

    sql =  text("DELETE FROM conversations WHERE topic_id IN (:topic_id)")
    db.session.execute(sql, {"topic_id":topic_id})

    sql =  text("DELETE FROM topics WHERE id=:id")
    db.session.execute(sql, {"id":topic_id})

    db.session.commit()