# BiblioteKA:books:

## Project Description

The BiblioteKA Project is a backend application that simulates a library's daily management tasks, providing access to two types of users: Students and Employees. Each user has their own set of permissions, allowing them to borrow, return, and track books according to the library's rules.

The project was developed using Python with the implementation of Generic Views, Model Serializer, and a Postgres database. It was presented as a final project for Module 5 at Kenzie Academy.


## Installation Instructions

- Check if you have Python installed: If you don't already have Python installed on your system, you can download it from the official Python website: **[Python](https://www.python.org/downloads/)**

- Install Poetry: To install the Poetry package manager, check if it is already installed globally by running **`poetry --version`**. If it is not installed, follow the instructions here: **[Poetry](https://github.com/asdf-community/asdf-poetry)**

- Install project dependencies: Once you have installed Poetry and cloned the project to your local machine, navigate to the project's root directory in your terminal and run the command **`poetry install`**. This will read the project's "pyproject.toml" file and install all the dependencies listed there

- Activate a virtual environment (optional): It's advisable to install the project's dependencies within a virtual environment to avoid conflicts with other packages on your system. To activate a virtual environment with Poetry, run the command **`poetry shell`** before installing the project's dependencies


## Endpoints

| HTTP Method | Description | Endpoint | User Types | Authentication Required |
| --- | --- | --- | --- | --- |
| POST | Create User | `/api/users/` | Students and Employees | No Authentication |
| POST | Login | `/api/users/login/` | Students and Employees | No Authentication |
| POST | Create Book | `/api/books/` | Employees | Authenticated |
| GET | List All Books | `/api/books/` | Students and Employees | Authenticated |
| POST | Loan Book | `/api/books/book_id/loans/` | Students and Employees | Authenticated |
| PATCH | Return Book | `/api/loans/loan_id/return/` | Students and Employees | Authenticated |
| GET | List User's Loans | `/api/users/loans/` | Students and Employees | Authenticated |
| GET | List All Loans | `/api/loans/all` | Employees | Authenticated |
| POST | Follow Book | `/api/book/book_id/following/` | Students and Employees | Authenticated |
| GET | List All Follows | `/api/following/` | Employees | Authenticated |
| GET | List User's Follows | `/api/users/following/` | Students and Employees | Authenticated |
| DELETE | Unfollow Book | `/api/book/book_id/following/` | Students and Employees | Authenticated |


## Application Rules

- A user can borrow a book for a period of 7 days
- If the book is not returned by the expected due date, the user will be blocked from borrowing any new books until the book is returned
- A blocked user can only borrow new books after 3 days of penalty, calculated from the day the delayed book is returned
- If the return date is on the weekend, the due date will be adjusted to the next weekday
- When a book is returned, all of its followers will receive an email notification about its availability


## Documentation

Access the application documentation using the following link:
**[Documentation](http://127.0.0.1:8000/api/docs/swagger/)**


## Deploy

Check out the application deploy using the link below:
**[Documentation](http://127.0.0.1:8000/api/docs/swagger/)**
