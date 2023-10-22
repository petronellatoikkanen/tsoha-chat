from db import db
import users, secret_topics
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT id, secret_message FROM secret_messages")
    result = db.session.execute(sql)
    return result.fetchall()

def get_list_by_topic(secret_topic_id):
    sql = text("SELECT M.sent_at, M.secret_message, U.username FROM secret_messages M, users U, secret_topics T WHERE M.user_id=U.id AND M.secret_topic_id=T.id AND M.secret_topic_id=:secret_topic_id  GROUP BY M.id, M.sent_at, M.secret_message, U.username ORDER BY M.sent_at DESC")
    result = db.session.execute(sql, {"secret_topic_id": secret_topic_id})
    return result.fetchall()

def get_user_messages(user_id):
    sql = text("SELECT M.id, M.secret_message, T.secret_topic FROM secret_messages M LEFT JOIN secret_topics T ON M.secret_topic_id=T.id WHERE m.user_id=:user_id GROUP BY M.id, T.secret_topic ORDER BY M.secret_topic_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def send_secret_message(secret_message, secret_topic):
    user_id = users.user_id()
    if user_id == 0:
        return False
    else:
        secret_topic_id = secret_topics.get_secret_topic_id(secret_topic)[0]

        sql = text("INSERT INTO secret_messages (secret_message, user_id, sent_at, secret_topic_id) VALUES (:secret_message, :user_id, NOW(), :secret_topic_id)")
        db.session.execute(sql, {"secret_message":secret_message, "user_id":user_id, "secret_topic_id":secret_topic_id})
        db.session.commit()
    return True


def alter_message(secret_message, secret_message_id):
    sql = text("UPDATE secret_messages SET secret_message=:secret_message WHERE id=:secret_message_id")
    db.session.execute(sql, {"secret_message":secret_message, "secret_message_id":secret_message_id})
    db.session.commit()
    return True


def delete_secret_message(secret_message_id):
    sql =  text("DELETE FROM secret_messages WHERE id=:secret_message_id")
    db.session.execute(sql, {"secret_message_id":secret_message_id})
    db.session.commit()