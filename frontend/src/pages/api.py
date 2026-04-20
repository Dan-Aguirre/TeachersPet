import requests

# base url for the flask backend -- make sure its running on 5000
BASE = "http://localhost:5000"


def login(username, password):
    # send login request and recieve user dict back
    try:
        res = requests.post(f"{BASE}/api/login", json={
            "username": username,
            "password": password
        })
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None  # backend probly not running


def register(username, password, role):
    # create new account -- role shud be 'student' or 'teacher'
    try:
        res = requests.post(f"{BASE}/api/register", json={
            "username": username,
            "password": password,
            "role":     role,
            "description": ""
        })
        if res.status_code == 201:
            return res.json()
        return None
    except:
        return None


def get_stats(uid):
    # grab full stats for a user -- points games streak etc
    try:
        res = requests.get(f"{BASE}/api/stats/{uid}")
        if res.status_code==200:
            return res.json()
        return None
    except:
        return None


def get_rankings():
    # global leaderboard sorted by points
    try:
        res = requests.get(f"{BASE}/api/rankings")
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None


def get_classes(uid):
    # returns dict w/ 'teaching' and 'enrolled' lists
    try:
        res = requests.get(f"{BASE}/api/classes/{uid}")
        if res.status_code==200:
            return res.json()
        return None
    except:
        return None


def get_class_members(class_id):
    # list of students in a class w/ their points
    try:
        res = requests.get(f"{BASE}/api/classes/{class_id}/members")
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None


def update_user(uid, **fields):
    # update user fields -- pass description= or password= as kwargs
    # tried doing a PUT but backend uses POST so keeping it
    try:
        res = requests.post(f"{BASE}/api/users/{uid}", json=fields)
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None


def get_question(difficulty):
    # fetch a random question at given difficulty
    try:
        res = requests.get(f"{BASE}/api/question", params={"difficulty": difficulty})
        if res.status_code==200:
            return res.json()
        return None
    except:
        return None


def submit_answer(user_id, question_id, answer):
    # submit answer and get back points earned + total
    try:
        res = requests.post(f"{BASE}/api/answer", json={
            "user_id":     user_id,
            "question_id": question_id,
            "answer":      answer
        })
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None


def join_class(code, student_id):
    # enroll student in class using join code
    try:
        res = requests.post(f"{BASE}/api/classes/join", json={
            "code":       code,
            "student_id": student_id
        })
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None


def create_class(teacher_id, name):
    # teacher creates a new class -- backend generates the join code
    try:
        res = requests.post(f"{BASE}/api/classes", json={
            "teacher_id": teacher_id,
            "name":       name
        })
        if res.status_code == 201:
            return res.json()
        return None
    except:
        return None


def logout(uid):
    # notify backend of logout (session cleanup)
    try:
        res = requests.post(f"{BASE}/api/logout", json={"user_id": uid})
        return res.status_code == 200
    except:
        return True  # still logout locally even if backend fails
    
def get_badges(uid):
    # get information about which badges student has
    try:
        res = requests.get(f"{BASE}/api/badges/{uid}")
        if res.status_code == 200:
            return res.json()
        return None
    except:
        None

        
