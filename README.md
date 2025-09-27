AI Study Planner

A desktop-based study planner built with Python and Tkinter to help students organize and manage study tasks effectively. It provides features for secure authentication, task creation, deadline tracking, and productivity monitoring, enabling better time management and study planning.

Features

User Authentication – Secure registration and login with hashed passwords.

Task Management – Add tasks with subject, topic, deadline, estimated time, and priority.

Task Tracking – View, update, and mark tasks as completed.

Automated Scheduling – Generates a study plan sorted by deadlines and priorities.

Productivity Statistics – Summarizes tasks by priority levels.

Data Persistence – Stores user data locally using JSON files.

Technology Stack

Python 3

Tkinter (GUI)

JSON (data storage)

Hashlib (password security)

Installation

Clone the repository:

git clone https://github.com/your-username/Study_Planner.git
cd Study_Planner


(Optional) Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Run the application:

python studyPlanner.py

Usage

Launch the application and register or log in.

Add study tasks with deadlines and priorities.

View, manage, and complete tasks from the dashboard.

Open the "Plan" tab to view the automatically generated study schedule.

Review progress in the "Stats" tab.

Project Structure
Study_Planner/
│── studyPlanner.py      # Main application
│── users.json           # Stores user credentials (hashed)
│── <username>_data.json # Stores individual user tasks
│── README.md            # Documentation
│── .gitignore           # Ignored files and secrets

Security Notes

Secrets such as API keys must not be committed to the repository.

Use a .env file (excluded via .gitignore) to store sensitive information.
