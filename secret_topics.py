from db import db
import users
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT id, secret_topic from secret_topics where visible = 1")
    result = db.session.execute(sql)
    return result.fetchall()


def get_secret_topic_id(secret_topic):
    sql = text("SELECT id, secret_topic from secret_topics where visible = 1 and secret_topic=:secret_topic")
    result = db.session.execute(sql, {"secret_topic":secret_topic})
    secret_topic = result.fetchone()
    return secret_topic[0]


def index_list(user_id):
    sql = text("SELECT T.secret_topic from secret_topics T, secret_topics_users U where T.id=U.secret_topic_id AND U.user_id=:user_id AND T.visible = 1 group by T.secret_topic")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()


def create_secret_topic(secret_topic):
    creator_user_id = users.user_id()
    if creator_user_id == 0:
        return False
    sql = text("INSERT INTO secret_topics (secret_topic, creator_user_id, created) VALUES (:secret_topic, :creator_user_id, NOW())")
    try: 
        db.session.execute(sql, {"secret_topic":secret_topic, "creator_user_id":creator_user_id})
        db.session.commit()
        return True
    except:
        return False

def add_secret_topic_user(secret_topic_id, user_id):
    sql = text("INSERT INTO secret_topics_users (secret_topic_id, user_id) VALUES (:secret_topic_id, :user_id)")
    db.session.execute(sql, {"secret_topic_id":secret_topic_id, "user_id":user_id,})
    db.session.commit()


def remove_secret_topic(secret_topic_id):
    ## kun poistaa keskustelualueen, niin myös alueen keskusteluihin ja viesteihin visiblen arvoksi 0
    sql =  text("UPDATE aecrettopics SET visible=0 WHERE id=:id")
    db.session.execute(sql, {"id":topic_id})
    db.session.commit()