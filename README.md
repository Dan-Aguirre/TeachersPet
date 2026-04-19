# Teacher'sPet
Project for CEN3031


## How to run the app

### Option 1 - Python (recomended)
make sure you have python installed first

1. install dependancies
```
pip install customtkinter requests flask flask-cors
```

2. start the backend (open a terminal and run this)
```
python Backend/backend.py
```

3. open another terminal and start the desktop app
```
python launcher.py
```

### Option 2 - run.py (easiest way)
does everything automaticly - installs deps, sets up db, starts backend and app

```
python run.py
```

### Option 3 - npm
make sure python and node are both installed first

1. install python dependancies
```
pip install -r requirements.txt
```

2. open Terminal 1 and start the backend
```
npm run backend
```

3. open Terminal 2 and start the app
```
npm start
```

> note: npm start just calls python under the hood so python still needs to be installed

---


## BACKEND INFO:
To Setup DB: `python3 setup_db.py`

### Backend API Commands:
Register
`curl -X POST http://localhost:5000/api/register -H "Content-Type: application/json" -d '{"username":"[USERNAME]","password":"[PASSWORD]","role":"[ROLE]"}'`

Login
`curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d '{"username":"[USERNAME]","password":"[PASSWORD]"}'`

Get User
`curl http://localhost:5000/api/users/[USER_ID]`

Update Username
`curl -X POST http://localhost:5000/api/users/[USER_ID] -H "Content-Type: application/json" -d '{"username":"[NEW_USERNAME]"}'`

Get Question
`curl http://localhost:5000/api/question?difficulty=[DIFFICULTY]`

Submit Answer
`curl -X POST http://localhost:5000/api/answer -H "Content-Type: application/json" -d '{"user_id":[USER_ID],"question_id":[QUESTION_ID],"answer":[ANSWER]}'`

Get Stats
`curl http://localhost:5000/api/stats/[USER_ID]`

Rankings
`curl http://localhost:5000/api/rankings`

Add Friend
`curl -X POST http://localhost:5000/api/friends -H "Content-Type: application/json" -d '{"user_id":[USER_ID],"friend_username":"[USERNAME]"}'`

Get Friends
`curl http://localhost:5000/api/friends/[USER_ID]`

Remove Friend
`curl -X DELETE http://localhost:5000/api/friends -H "Content-Type: application/json" -d '{"user_id":[USER_ID],"friend_id":[FRIEND_ID]}'`

Create Class
`curl -X POST http://localhost:5000/api/classes -H "Content-Type: application/json" -d '{"teacher_id":[USER_ID],"name":"[CLASS_NAME]"}'`

Join Class
`curl -X POST http://localhost:5000/api/classes/join -H "Content-Type: application/json" -d '{"student_id":[USER_ID],"code":"[CLASS_CODE]"}'`

Get My Classes
`curl http://localhost:5000/api/classes/[USER_ID]`

Get Class Members
`curl http://localhost:5000/api/classes/[CLASS_ID]/members`
