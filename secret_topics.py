from db import db
import users
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT id, secret_topic from secrettopics where visible = 1")
    result = db.session.execute(sql)
    return result.fetchall()

def indexinfo():
    # hakua pitää muokata
    sql = text("select topics.topic, COALESCE(count(conversations.topic_name), 0), COALESCE(count(messages.content), 0), COALESCE(NULLIF(MAX(messages.sent_at), NULL), NULL) from topics left join conversations on topics.topic=conversations.topic_name left join messages on conversations.convo=messages.convo_name where topics.visible=1 group by topics.id")
    result = db.session.execute(sql)
    return result.fetchall()

def create_secret_topic(secret_topic, users_list):
    creator_user_id = users.user_id()
    if creator_user_id == 0:
        return False
    for user in users_list:
        users_user_id =  user
        sql = text("INSERT INTO secrettopics (secret_topic, creator_user_id, users_user_id, created) VALUES (:secret_topic, :creator_user_id, :users_user_id, NOW())")
        db.session.execute(sql, {"secret_topic":secret_topic, "creator_user_id":creator_user_id, "users_user_id":users_user_id})

    db.session.commit()
    return True


def remove_secret_topic(secret_topic_id):
    ## kun poistaa keskustelualueen, niin myös alueen keskusteluihin ja viesteihin visiblen arvoksi 0
    sql =  text("UPDATE aecrettopics SET visible=0 WHERE id=:id")
    db.session.execute(sql, {"id":topic_id})
    db.session.commit()