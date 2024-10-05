from db.session import engine
from models import project, activity, user, achievements, streak    

def init_db():
    project.Base.metadata.create_all(bind=engine)
    activity.Base.metadata.create_all(bind=engine)
    user.Base.metadata.create_all(bind=engine)
    achievements.Base.metadata.create_all(bind=engine)
    streak.Base.metadata.create_all(bind=engine)    

if __name__ == "__main__":
    init_db()
    print("Database initialized.")