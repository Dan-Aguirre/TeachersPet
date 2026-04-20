from flask import Flask, jsonify, request, Response
import sqlite3, random, string, bcrypt
from datetime import date, timedelta

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
    # grab description if they sent one, default empty string
    desc = d.get("description", "")
    try:
        con = get_db()
        hashed = bcrypt.hashpw(d["password"].encode(), bcrypt.gensalt()).decode()
        con.execute(
            "INSERT INTO users (username, password, role, description) VALUES (?, ?, ?, ?)",
            (d["username"], hashed, d.get("role", "student"), desc),
        )
        con.commit()
        usr_data = con.execute(
            "SELECT * FROM users WHERE username=?", (d["username"],)
        ).fetchone()
        return jsonify(dict(usr_data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/login", methods=["POST"])
def login():
    d = request.json
    con = get_db()
    user = con.execute(
        "SELECT * FROM users WHERE username=?",
        (d["username"],),
    ).fetchone()
    if not user or not bcrypt.checkpw(d["password"].encode(), user["password"].encode()):
        return jsonify({"error": "Wrong username or password"}), 401

    # streak logic -- check last login date and update accordingly
    today     = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    last = user["last_login"]
    cur_streak = user["streak"]

    if last == today:
        new_streak = cur_streak  # already logged in today, dont increment
    elif last == yesterday:
        new_streak = cur_streak+1  # consecutive day -- keep it going
    else:
        new_streak = 1  # missed a day or brand new user, reset

    con.execute(
        "UPDATE users SET streak=?, last_login=? WHERE id=?",
        (new_streak, today, user["id"])
    )
    con.commit()
    # re-fetch so we return the updated values
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
    # update whatever fields they sent -- username password or description
    if "username" in d:
        con.execute("UPDATE users SET username=? WHERE id=?", (d["username"], uid))
    if "password" in d:
        hashed = bcrypt.hashpw(d["password"].encode(), bcrypt.gensalt()).decode()
        con.execute("UPDATE users SET password=? WHERE id=?", (d["password"], uid))
    if "description" in d:
        con.execute("UPDATE users SET description=? WHERE id=?", (d["description"], uid))
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
    # try to parse answer as float -- shud always be a number
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

    #If answer was right add 1 to answer streak, otherwise set it to zero
    if pts > 0:
        con.execute("UPDATE users SET answer_streak = answer_streak + 1 WHERE id=?",(uid,))
    else:
        con.execute("UPDATE users SET answer_streak = 0 WHERE id=?", (uid,))

    #Check if user unlocked a badge
    user = con.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    new_streak = user["answer_streak"]

    #Kind of repetitive as it checks for every badge everytime (could start from latest badge), but
    #this is the easier way to do it and it works fine as we don't have many to check
    for badge in [5, 10, 20, 50, 75, 100, 150, 200]:
        if new_streak >=badge:
            con.execute(f"UPDATE users SET badge_{badge} = 1 WHERE id=?", (uid,))

    con.commit()

    total = con.execute("SELECT points FROM users WHERE id=?", (uid,)).fetchone()["points"]
    response = {
        "correct_answer": correct,
        "your_answer": given,
        "exact": exact,
        "points_earned": pts,
        "total_points": total,
    }

    # If answer was correct, generate a new question with same difficulty
    if exact:
        new_question = con.execute(
            "SELECT id, question, difficulty FROM questions WHERE difficulty=?", (diff,)
        ).fetchall()
        if new_question:
            new_q = dict(random.choice(new_question))
            response["next_question"] = new_q

    response["answer_streak"] = user["answer_streak"]

    return jsonify(response)

# returns stats for streaks and badges
@app.route("/api/badges/<int:uid>", methods=["GET"])
def get_badges(uid):
    con = get_db()
    user = con.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    if not user:
        return jsonify({"error": "not found"}), 404
    return jsonify({
        "answer_streak": user["answer_streak"],
        "badge_5":   user["badge_5"],
        "badge_10":  user["badge_10"],
        "badge_20":  user["badge_20"],
        "badge_50":  user["badge_50"],
        "badge_75":  user["badge_75"],
        "badge_100": user["badge_100"],
        "badge_150": user["badge_150"],
        "badge_200": user["badge_200"],
    })


# returns stats for a user -- games played, total points, streak etc
@app.route("/api/stats/<int:uid>", methods=["GET"])
def stats(uid):
    con = get_db()
    # session stats
    row = con.execute(
        "SELECT COUNT(*) games, SUM(points) total FROM sessions WHERE user_id=?",
        (uid,),
    ).fetchone()
    # also grab user info for streak and description
    usr_data = con.execute(
        "SELECT username, points, streak, description FROM users WHERE id=?", (uid,)
    ).fetchone()
    if not usr_data:
        return jsonify({"error": "not found"}), 404

    # merge the two rows into one response dict
    res = {
        "id": uid,
        "username": usr_data["username"],
        "points": usr_data["points"],
        "games_played": row["games"] or 0,
        "streak": usr_data["streak"],
        "description": usr_data["description"],
    }
    return jsonify(res)


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
    return jsonify({
        "teaching": [dict(r) for r in teaching],
        "enrolled": [dict(r) for r in enrolled],
    })


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
    app.run(debug=True, port=5000, host = "0.0.0.0")
