# File Sensitivity System

## Code Challenge Problem Statement

A user would like to create a system that is able to save files and analyze the files’ sensitivity score. The system should allow listing the files together with each file’s sensitivity score. As the files may be sensitive, users using the system will be required to register and authenticate themselves before being able to utilise the system’s features. The sensitivity score of a file is defined in later sections.

### Task Summary

You will be required to create two applications.

- Create a web application that exposes REST API that contain endpoints fulfilling the following requirements:
  - User Registration
    - Save basic user information
    - Password must be encrypted
  - Token Authentication
    - Authenticate user by username and password
    - Return a JSON Web Token (JWT)
  - Upload File
    - Token authentication required
    - It should only accept .txt file s
    - Save the file locally and save the file name, file size and file path into database
  - List Files
    - Token authentication required
    - List all the file information in database
  - Any other endpoints which you deem necessary
  
  
- Create a Celery application to handle a single asynchronous task that is run periodically. The task should do the following:
  - Retrieve all file information from the database
  - Read the file content of each file
  - Calculate the sensitivity score of a file
  - Update the value of the sensitivity score and last updated timestamp of the file inside the database
 
You may choose any python web framework or database for your assignment although we prefer to have Flask / Django for web framework and Postgres as your RDBMS. Being able to Dockerize your application and launching the stack with Docker Compose will be a bonus. Make sure your code follows the OOP principles.  

---

### Calculating Sensitivity Score

Given a sensitivity table:

| Sensitive Word | Score |
|----------------|-------|
| Secret         | 10    |
| Dathena        | 7     |
| Internal       | 5     |
| External       | 3     |
| Public         | 1     |

Based on the sensitivity table provided, the formula for the sensitivity score of a file is the sum of scores for every word (from the table) found in the file.

Example file content:

```
This is a top secret file.

All these information are not meant to be external purposes.

Regards,
Joker.
Dathena
```

In this case, the sensitivity score for this document should be calculated as:

```
Sensitive words found = (Secret: 10), (external: 3), (Dathena: 7)

Total sensitivity score = 10 + 3 + 7 = 20
```

## Getting Started

### Prerequisites

This project is run on python 3.8.10 and postgres 13.4.

### Installation

Clone repository.

``` bash
git clone https://github.com/DavidLHW/file-sensitivity-system.git
```

Install dependencies.

``` bash
pip install -r requirements.txt
```

### Source Tree
``` bash
.
├── flaskapp/
│   ├── flask_app.py
│   └──  api/
│       ├── conf/
│       ├── database/
│           └── ...
│       └── .../
│           └── ...
├── celeryapp/
│   ├── celery_app.py
│   ├── celeryconfig.py
│   ├── tasks.py
│   ├── scoreconfig.json
│   └── ...
└── files/
    ├── UPLOADED_FILE_1.txt
    ├── UPLOADED_FILE_2.txt
    ├── UPLOADED_FILE_3.txt
    └── ...
```


## Flask App Usage

A simple web app that exposes REST API.

Navigate to ./flaskapp

To initialise the app, execute the following command.

``` bash
python ./flask_app.py
```

### Routes

PROJECT_URL is default to localhost:5000

Register a new user.

``` curl
curl --location --request POST 'http://PROJECT_URL/api/auth/register' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer ACCESS_TOKEN' \
--data-raw '{
  "username":"test_user",
  "email":"test_email@example.com",
  "password":"test_password"
}'
```

Login to an existing user account.

``` curl
curl --location --request POST 'http://PROJECT_URL/api/auth/login' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer ACCESS_TOKEN' \
--data-raw '{
  "email":"test_email@example.com",
  "password":"test_password"
}'
```

Logout of an existing session.

``` curl
curl -H "Content-Type: application/json" \
--header "Authorization: Bearer ACCESS_TOKEN" \
--data '{"refresh_token":"REFRESH_TOKEN"}' \
http://localhost:5000/api/auth/logout
```

Upload file to app.

``` curl
curl --location --request POST 'http://PROJECT_URL/api/file' \
--header 'Authorization: Bearer ACCESS_TOKEN' \
--form 'file=@"/C:/path/to/file/text.txt"'
```

Get all file information.

``` curl
curl --location --request GET 'http://PROJECT_URL/api/files' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer ACCESS_TOKEN'
```

## Celery App Usage

Navigate to ./celeryapp

To initialise the Celery worker, execute the following command.
``` bash
celery -A tasks worker --pool=solo -l info
```

To initialise Celery app to calculate scores of all files in db, execute the following command.

``` bash
python ./celery_app.py
```
