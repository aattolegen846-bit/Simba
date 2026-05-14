"""Master seed: runs A1 + A2 + B1 + B2 + C1 curriculum seeds."""
import os
os.environ.setdefault("SECRET_KEY", "dev")
os.environ.setdefault("WEBHOOK_SECRET", "dev")

from app.main import create_app
from app.database import db

app = create_app()

with app.app_context():
    db.create_all()
    print("🌱 Seeding SIMBA full curriculum (A1 → C1)...\n")

    from seed_a1 import seed_a1
    seed_a1()

    from seed_a2 import seed_a2
    seed_a2()

    from seed_b1 import seed_b1
    seed_b1()

    from seed_b2 import seed_b2
    seed_b2()

    from seed_c1 import seed_c1
    seed_c1()

    print("\n🎉 Full curriculum seeded successfully!")
    print("   A1: 11 lessons — Greetings, Family, Numbers, Colors, Food, Routines")
    print("   A2: 10 lessons — Past Tense, Hobbies, Shopping, Travel, Emotions")
    print("   B1: 10 lessons — Present Perfect, Modals, Conditionals, Passive Voice")
    print("   B2: 10 lessons — Reported Speech, Idioms, Relative Clauses, Perfect Tenses")
    print("   C1: 10 lessons — Mixed Conditionals, Inversion, Academic Writing, Phrasal Verbs")
    print("   Total: 51 lessons, 260+ real tasks with Kazakh translations")
