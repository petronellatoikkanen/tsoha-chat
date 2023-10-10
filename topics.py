from db import db
import users
from sqlalchemy.sql import text

def get_list():
    sql = text("SELECT id, topic from topics where visible = 1")
    result = db.session.execute(sql)
    return result.fetchall()

def indexinfo():
    # hakua pitää muokata
    sql = text("select topics.topic, COALESCE(count(conversations.topic_name), 0), COALESCE(count(messages.content), 0), COALESCE(NULLIF(MAX(messages.sent_at), NULL), NULL) from topics left join conversations on topics.topic=conversations.topic_name left join messages on conversations.convo=messages.convo_name where topics.visible=1 group by topics.id")
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


def remove_topic(topic_id):
    ## kun poistaa keskustelualueen, niin myös alueen keskusteluihin ja viesteihin visiblen arvoksi 0
    sql =  text("UPDATE topics SET visible=0 WHERE id=:id")
    db.session.execute(sql, {"id":topic_id})
    db.session.commit()