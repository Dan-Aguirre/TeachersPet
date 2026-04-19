import sqlite3
import bcrypt

con = sqlite3.connect("game.db")

# setup all the tables -- run this first before starting backend
con.executescript("""
CREATE TABLE IF NOT EXISTS users (
	id       INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	role     TEXT NOT NULL DEFAULT 'student',
	points   INTEGER NOT NULL DEFAULT 0,
	streak   INTEGER NOT NULL DEFAULT 0,
    description TEXT NOT NULL DEFAULT '',
    last_login  TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS questions (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    question   TEXT NOT NULL,
    answer     REAL NOT NULL,
    difficulty TEXT NOT NULL DEFAULT 'easy'
);

CREATE TABLE IF NOT EXISTS sessions (
	id          INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id     INTEGER NOT NULL,
	question_id INTEGER NOT NULL,
	answer      REAL,
	points      INTEGER NOT NULL DEFAULT 0,
	played_at   TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS friends (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL,
    friend_id INTEGER NOT NULL,
    UNIQUE(user_id, friend_id)
);

CREATE TABLE IF NOT EXISTS classes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    name       TEXT NOT NULL,
    code       TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS enrollments (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id   INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    UNIQUE(class_id, student_id)
);
""")

# seed some test users if they dont exist yet
try:
    pw1 = bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode()
    pw2 = bcrypt.hashpw(b"secret", bcrypt.gensalt()).decpde()
    con.execute("INSERT INTO users (username, password, role) VALUES ('student1', 'password123', 'student')")
    con.execute("INSERT INTO users (username, password, role) VALUES ('teacher1', 'secret', 'teacher')")
except:
    pass  # already seeded, skip

# seed some questions -- easy medium hard
# tried doing this dynamically but just hardcoding is fine for now
questions = [
    ("What is 5 + 3?", 8, "easy"),
    ("What is 10 - 4?", 6, "easy"),
    ("What is 7 + 9?", 16, "easy"),
    ("What is 15 - 7?", 8, "easy"),
    ("What is 6 x 7?", 42, "medium"),
    ("What is 8 x 9?", 72, "medium"),
    ("What is 48 / 6?", 8, "medium"),
    ("What is 3x + 5 = 20, solve for x?", 5, "medium"),
    ("What is 12 x 13?", 156, "hard"),
    ("Solve: 2x^2 = 50, x > 0?", 5, "hard"),
    ("What is (3/4) + (5/8)?", 1.375, "hard"),
    ("Solve: 4x - 7 = 3x + 6?", 13, "hard"),
]

for q, a, d in questions:
    try:
        con.execute("INSERT INTO questions (question, answer, difficulty) VALUES (?, ?, ?)", (q, a, d))
    except:
        pass

con.commit()
con.close()
print("done: db=game.db")
