# Finish it! Documentation

## About the app

The *Finish It!* app can be used for keeping track of courses and books that you would like to complete.
You can also create tags and assign them to the items (books and courses), which can be used for categorising them.

In the app, you can keep track of the current status of completion (for example, *Not Started* or *Completed*) and how important it is to complete the item (the priority).
Unlike a todo list, there are no due dates, sub-tasks or assignment of the items to users to complete.
The purpose of the app is to keep track of books and courses that are likely to be useful for long-term career or personal goals rather than tasks that need to be completed in the short-term.

The app will not be open for anyone to sign up for.
Administrator users will be able to create and manage users in the app, as well as manage their items and tags.
Users will only be able to removed from the systems if they have no items (books and courses) or tags in the system.

For more details about the app's design, see the `design_notes.md` file.

## Running the app

There are three main steps you will need to complete before running the *Finish It!* app.

### Step 1. Install dependencies with pip

We recommend using a virtual environment to manage the app's dependencies.
Once you have created and activated the virtual environment for this app, run the appropriate command for installing from the requirements file.
On Mac this is: `python -m pip install -r requirements.txt` and on Windows: `py -m pip install -r requirements.txt`.
For more details about this step, see the [Requirement Files section in the pip docs](https://pip.pypa.io/en/stable/user_guide/#requirements-files).

### Step 2. Create a file for required environment variables

This app uses the [python-dotenv](https://pypi.org/project/python-dotenv/) for loading environment variables from a file, rather than setting this in the command line or in system settings.
You may notice that there are no explicit imports to the *python-dotenv* module or methods. Flask will automatically load the environment variables if the *python-dotenv* module has been installed, as explained [here in the Flask docs](https://flask.palletsprojects.com/en/2.0.x/cli/#environment-variables-from-dotenv).

The .env file is not included in the git repository because it can contain passwords or other sensitive information.
To run the app, you will need to create a file titled `.env` in same directory as this `README` file.

The required variables in the `.env` file are described in the table below with some example values.
Where there are no `<>` tags in the example value, that value should be used in the file.
Note that usernames and emails have to be unique, so values for the `person_*` and `admin_*` variables should be different.

| Name            | Value                    |
|-----------------|--------------------------|
| DEBUG           | True                     |
| FLASK_ENV       | development              |
| FLASK_APP       | finish.py                |
| person_username | \<your name\>            |
| person_password | \<any password\>         |
| person_email    | \<your email\>           |
| admin_username  | admin                    |
| admin_password  | \<any password\>         |
| admin_email     | \<your secondary email\> |

### Step 3. Run the init-db command to create and seed database

Once you have created the `.env` file and set up the different environment variables, you will be able to run the command to create a database for the app and insert some initial data into the tables.

Before running the command,

From the command line, run the command `flask init-db` and you should receive a message saying that the database has been initalised successfully.
If you receive an error about a module being not found, make sure you have activated the virtual environment and installed the dependencies correctly (described in Step 1).
If you receive an error about a NoneType, you may be missing one of the environment variables described in Step 2.

Once you have created and seeded the database, you will be able to run the app with the `flask run` command and view it from the address flask hosts it on (the default is 127.0.0.1:500).
You can check if the database has been created successfully and contains data by opening the `app.db` file with a SQLite viewing app, such as [DB Browser for SQLite](https://sqlitebrowser.org/).