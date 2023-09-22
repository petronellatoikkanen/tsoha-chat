from db import db
import users
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT T.topic, U.username, T.created FROM topics T, users U WHERE T.user_id=U.id ORDER BY T.id")
    result = db.session.execute(sql)
    return result.fetchall()

def create_topic(topic):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO topics (topic, user_id, created) VALUES (:topic, :user_id, NOW())")
    db.session.execute(sql, {"topic":topic, "user_id":user_id})
    db.session.commit()
    return True