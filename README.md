# Teacher'sPet
Project for COP4600




## BACKEND INFO:
To Setup DB: `python3 setup_dp.py`

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
