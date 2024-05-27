# Medical Security System

Medical Security System is a simple app, where all informations about patients are stored in local blockchain. Users are stored
on local database, where they can keep informations about their blocks and in case of that, they don't have to remeber their block id's.

## Installation

### Requirements

Before app installation make sure, You have installed tools like:

- [Python](https://www.python.org/downloads/) (Python 3.x)
- [PostgreSQL](https://www.postgresql.org/download/) (Database)

### Repository Cloning

```bash
$ git clone https://github.com/Szoot/Medical-Security-System.git
$ cd Medical-Security-System
```
### Dependency Installation

```bash
$ python -m venv venv
$ source venv/bin/activate      # Unix/Linux
$ venv\Scripts\activate         # Windows
$ pip install -r requirements.txt
```

### Database Configuration

Change username, password, database_name to your local database config at `config.py` file.

```bash
DATABASE_URL=postgresql://username:password@localhost/database_name
```

### Launching The Application

Application will be available at `http://localhost:5000/`

```bash
$ flask run
```

