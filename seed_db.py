import os
os.environ["SECRET_KEY"] = "dev"
os.environ["WEBHOOK_SECRET"] = "dev"
from app.main import create_app
from app.database import db
from app.models.db_models import Course, Module, Lesson, Task

app = create_app()

def seed_db():
    print("Seeding DB...")
    from generate_curriculum import seed_level, levels
    with app.app_context():
        db.create_all()
        Task.query.delete()
        Lesson.query.delete()
        Module.query.delete()
        Course.query.delete()
        db.session.commit()
        for title, code, topics in levels:
            print("Generating", title)
            seed_level(title, code, topics)
        db.session.commit()
        print("Done!")

if __name__ == "__main__":
    seed_db()
