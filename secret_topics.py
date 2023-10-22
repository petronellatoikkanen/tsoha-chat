from db import db
import users
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT id, secret_topic from secret_topics ")
    result = db.session.execute(sql)
    return result.fetchall()


def get_secret_topic_id(secret_topic):
    sql = text("SELECT id from secret_topics where secret_topic=:secret_topic")
    result = db.session.execute(sql, {"secret_topic":secret_topic})
    return result.fetchone()


def index_list(user_id):
    sql = text("SELECT T.secret_topic from secret_topics T, secret_topics_users U where T.id=U.secret_topic_id AND U.user_id=:user_id group by T.secret_topic")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()


def create_secret_topic(secret_topic):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = text("INSERT INTO secret_topics (secret_topic, user_id, created_at) VALUES (:secret_topic, :user_id, NOW())")
    try: 
        db.session.execute(sql, {"secret_topic":secret_topic, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

def add_secret_topic_user(secret_topic_id, user_id):
    sql = text("INSERT INTO secret_topics_users (secret_topic_id, user_id) VALUES (:secret_topic_id, :user_id)")
    db.session.execute(sql, {"secret_topic_id":secret_topic_id, "user_id":user_id,})
    db.session.commit()


def remove_secret_topic(secret_topic_id):
    sql =  text("DELETE FROM secret_messages WHERE secret_topic_id IN (:secret_topic_id)")
    db.session.execute(sql, {"secret_topic_id":secret_topic_id})

    sql =  text("DELETE FROM secret_topics_users WHERE secret_topic_id IN (:secret_topic_id)")
    db.session.execute(sql, {"secret_topic_id":secret_topic_id})

    sql =  text("DELETE FROM secret_topics WHERE id=:secret_topic_id")
    db.session.execute(sql, {"secret_topic_id":secret_topic_id})
    db.session.commit()