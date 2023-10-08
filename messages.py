from db import db
import users, conversations
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id")
    result = db.session.execute(sql)
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
