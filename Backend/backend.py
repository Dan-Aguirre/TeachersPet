from flask import Flask, jsonify, request, Response
import sqlite3, random, string

app = Flask(__name__)


def get_db():
    con = sqlite3.connect("game.db", check_same_thread=False, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    return con


@app.after_request
def cors(r):
    r.headers["Access-Control-Allow-Origin"] = "*"
    r.headers["Access-Control-Allow-Headers"] = "Content-Type"
    r.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    return r


@app.route("/", defaults={"p": ""}, methods=["OPTIONS"])
@app.route("/<path:p>", methods=["OPTIONS"])
def preflight(p=""):
    return Response(status=200)


@app.route("/api/register", methods=["POST"])
def register():
    d = request.json
    try:
        con = get_db()
        con.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (d["username"], d["password"], d.get("role", "student")),
        )
        con.commit()
        user = con.execute(
            "SELECT * FROM users WHERE username=?", (d["username"],)
        ).fetchone()
        return jsonify(dict(user)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/login", methods=["POST"])
def login():
    d = request.json
    con = get_db()
    user = con.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (d["username"], d["password"]),
    ).fetchone()
    if not user:
        return jsonify({"error": "Wrong username or password"}), 401
    con.execute("UPDATE users SET streak = streak + 1 WHERE id=?", (user["id"],))
    con.commit()
    user = con.execute("SELECT * FROM users WHERE id=?", (user["id"],)).fetchone()
    return jsonify(dict(user))


@app.route("/api/users/<int:uid>", methods=["GET"])
def get_user(uid):
    con = get_db()
    user = con.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    if not user:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(user))


@app.route("/api/users/<int:uid>", methods=["POST"])
def update_user(uid):
    d = request.json
    con = get_db()
    if "username" in d:
        con.execute("UPDATE users SET username=? WHERE id=?", (d["username"], uid))
    if "password" in d:
        con.execute("UPDATE users SET password=? WHERE id=?", (d["password"], uid))
    con.commit()
    return jsonify(
        dict(con.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone())
    )


@app.route("/api/question", methods=["GET"])
def get_question():
    diff = request.args.get("difficulty", "easy")
    con = get_db()
    qs = con.execute(
        "SELECT id, question, difficulty FROM questions WHERE difficulty=?", (diff,)
    ).fetchall()
    if not qs:
        return jsonify({"error": "no questions found"}), 404
    return jsonify(dict(random.choice(qs)))


@app.route("/api/answer", methods=["POST"])
def submit_answer():
    d = request.json
    uid = d["user_id"]
    qid = d["question_id"]
    given = float(d["answer"])

    con = get_db()
    q = con.execute("SELECT * FROM questions WHERE id=?", (qid,)).fetchone()
    if not q:
        return jsonify({"error": "question not found"}), 404

    correct = q["answer"]
    exact = abs(given - correct) < 0.001
    diff = q["difficulty"]

    if exact:
        pts = {"easy": 10, "medium": 20, "hard": 40}.get(diff, 10)
    elif abs(given - correct) / max(abs(correct), 1) < 0.1:
        pts = {"easy": 5, "medium": 10, "hard": 20}.get(diff, 5)
    else:
        pts = 0

    con.execute(
        "INSERT INTO sessions (user_id, question_id, answer, points) VALUES (?, ?, ?, ?)",
        (uid, qid, given, pts),
    )
    con.execute("UPDATE users SET points = points + ? WHERE id=?", (pts, uid))
    con.commit()

    total = con.execute("SELECT points FROM users WHERE id=?", (uid,)).fetchone()[
        "points"
    ]
    return jsonify(
        {
            "correct_answer": correct,
            "your_answer": given,
            "exact": exact,
            "points_earned": pts,
            "total_points": total,
        }
    )


@app.route("/api/stats/<int:uid>", methods=["GET"])
def stats(uid):
    con = get_db()
    row = con.execute(
        """
        SELECT COUNT(*) games, SUM(points) total,
               SUM(CASE WHEN answer = (SELECT answer FROM questions WHERE id=question_id) THEN 1 ELSE 0 END) exact_correct
        FROM sessions WHERE user_id=?
    """,
        (uid,),
    ).fetchone()
    return jsonify(dict(row))


@app.route("/api/rankings", methods=["GET"])
def rankings():
    con = get_db()
    rows = con.execute(
        "SELECT id, username, role, points FROM users ORDER BY points DESC LIMIT 50"
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/friends/<int:uid>", methods=["GET"])
def get_friends(uid):
    con = get_db()
    rows = con.execute(
        """
        SELECT u.id, u.username, u.points FROM friends f
        JOIN users u ON u.id = f.friend_id WHERE f.user_id=?
    """,
        (uid,),
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/friends", methods=["POST"])
def add_friend():
    d = request.json
    con = get_db()
    friend = con.execute(
        "SELECT * FROM users WHERE username=?", (d["friend_username"],)
    ).fetchone()
    if not friend:
        return jsonify({"error": "user not found"}), 404
    try:
        con.execute(
            "INSERT INTO friends (user_id, friend_id) VALUES (?, ?)",
            (d["user_id"], friend["id"]),
        )
        con.execute(
            "INSERT INTO friends (user_id, friend_id) VALUES (?, ?)",
            (friend["id"], d["user_id"]),
        )
        con.commit()
        return jsonify({"message": f"added {friend['username']}"})
    except Exception:
        return jsonify({"error": "already friends"}), 400


@app.route("/api/friends", methods=["DELETE"])
def remove_friend():
    d = request.json
    con = get_db()
    con.execute(
        "DELETE FROM friends WHERE user_id=? AND friend_id=?",
        (d["user_id"], d["friend_id"]),
    )
    con.execute(
        "DELETE FROM friends WHERE user_id=? AND friend_id=?",
        (d["friend_id"], d["user_id"]),
    )
    con.commit()
    return jsonify({"message": "removed"})


@app.route("/api/classes", methods=["POST"])
def create_class():
    d = request.json
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    con = get_db()
    con.execute(
        "INSERT INTO classes (teacher_id, name, code) VALUES (?, ?, ?)",
        (d["teacher_id"], d["name"], code),
    )
    con.commit()
    cls = con.execute("SELECT * FROM classes WHERE code=?", (code,)).fetchone()
    return jsonify(dict(cls)), 201


@app.route("/api/classes/join", methods=["POST"])
def join_class():
    d = request.json
    con = get_db()
    cls = con.execute(
        "SELECT * FROM classes WHERE code=?", (d["code"].upper(),)
    ).fetchone()
    if not cls:
        return jsonify({"error": "class not found"}), 404
    try:
        con.execute(
            "INSERT INTO enrollments (class_id, student_id) VALUES (?, ?)",
            (cls["id"], d["student_id"]),
        )
        con.commit()
        return jsonify({"message": f"joined {cls['name']}", "class": dict(cls)})
    except Exception:
        return jsonify({"error": "already enrolled"}), 400


@app.route("/api/classes/<int:uid>", methods=["GET"])
def my_classes(uid):
    con = get_db()
    teaching = con.execute(
        "SELECT * FROM classes WHERE teacher_id=?", (uid,)
    ).fetchall()
    enrolled = con.execute(
        """
        SELECT c.* FROM enrollments e
        JOIN classes c ON c.id = e.class_id
        WHERE e.student_id=?
    """,
        (uid,),
    ).fetchall()
    return jsonify(
        {
            "teaching": [dict(r) for r in teaching],
            "enrolled": [dict(r) for r in enrolled],
        }
    )


@app.route("/api/classes/<int:class_id>/members", methods=["GET"])
def class_members(class_id):
    con = get_db()
    rows = con.execute(
        """
        SELECT u.id, u.username, u.points FROM enrollments e
        JOIN users u ON u.id = e.student_id
        WHERE e.class_id=?
        ORDER BY u.points DESC
    """,
        (class_id,),
    ).fetchall()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
