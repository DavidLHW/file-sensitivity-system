# file-management-system

## Problem Statement

A user would like to create a system that is able to save files and analyze the files’ sensitivity score. The system should allow listing the files together with each file’s sensitivity score. As the files may be sensitive, users using the system will be required to register and authenticate themselves before being able to utilise the system’s features. The sensitivity score of a file is defined in later sections.

### Dathena Code Challenge

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

## Getting Started

### Prerequisites

### Installation

## Usage

### Example
