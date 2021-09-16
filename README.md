# file-management-system

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

### Installation

## Usage

### Example
