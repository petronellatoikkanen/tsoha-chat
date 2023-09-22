from db import db
import users
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT C.convo, U.username, C.created_at FROM conversations C, users U WHERE C.user_id=U.id ORDER BY C.id")
    result = db.session.execute(sql)
    return result.fetchall()

def create_conversation(convo):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO conversations (convo, user_id, created_at) VALUES (:convo, :user_id, NOW())")
    db.session.execute(sql, {"convo":convo, "user_id":user_id})
    db.session.commit()
    return True