# Chess App

Retrieve and process data from the Chess.com API (https://www.chess.com/news/view/published-data-api#pubapi-endpoint-games).
Compare the results between Player 1 and their opponent (Player 2) throughout their game history.

## Getting Started

Below are all the instructions to successfully set up and run the project.

### Prerequisites

Requirements for the software and other tools to build, test and push 
- [Python](min.require: 3.7.0)
- [pip](Python package manager)

### Installing

A step by step series of examples that tell you how to get a development
environment running

Clone the repo

    clone <repository-url> 
    cd <repository-folder>

Set up a virtual environment

    python -m venv env
    # On Linux : source env/bin/activate 
    # On Windows: env\Scripts\activate

Install dependencies

    pip install -r requirements.txt
    
### Configuration & Usage

Set up Django

```
python manage.py migrate
```

Start the Django development server:

```
python manage.py runserver
```

Access the API

The API is exposed via endpoints for comparing players. Example:
```
http://127.0.0.1:8000/api/<username1>/<username2>/
```
Replace `<username1>` and `<username2>` with the Chess.com usernames of the players you wish to compare.
