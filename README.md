# Sport Hours Tracking

This project is online at http://10.90.138.82/ through the UniversityStudent network.

If you'd like to run the application locally, the following are the deployment instructions, assuming a Ubuntu 18.04 machine.



## Step 0. Prerequisites

Ensure you have Python 3.7:

```bash
sudo apt install python3.7-minimal
python3.7 --version
```

Ensure you have a running PostgreSQL server:

```bash
sudo apt install postgresql
sudo systemctl start postgresql
# the database configuration is left out
```

Install `pipenv` through `pip`:

```bash
sudo pip3 install pipenv
```

[Install Yarn](https://linuxize.com/post/how-to-install-yarn-on-ubuntu-18-04/) (will also install Node.js, if not present).

Install `nginx`:

```bash
sudo apt install nginx
```



## Step 1. Install dependencies

Install the backend dependencies with `pipenv` inside the `backend/` directory:

```bash
cd backend
pipenv install
cd ..
```

Install the frontend dependencies with `yarn` inside the `frontend/` directory:

```bash
cd frontend
yarn install
cd ..
```



## Step 2. Initialize the database

Create a database (say, `sport_hours`):

```sql
CREATE DATABASE sport_hours;
```

You may additionally need to set a password for your account (`user` in this case):

```sql
ALTER USER user PASSWORD 'your_desired_password';
```

Then upgrade the database to fill it with tables:

```bash
export DB_URL='postgresql://user:your_desired_password@localhost/sport_hours'
export FLASK_APP=run.py
cd backend
pipenv run flask db upgrade
cd ..
```

**Note**: change the `DB_URL` according to your situation.



## Step 3. Run the servers

You will need two terminal sessions. Over SSH, the preferred way is to use `tmux`:

* Connect to the `tmux` server:
  `tmux attach || tmux new`
* Use `Ctrl+B` and then `d` to detach from `tmux` and return to your terminal
* Use `Ctrl+B` and then `c` to create a new session (you'll need two)
* Use `Ctrl+B` and then `0` or `1` to switch between the two sessions



Launch Nginx with the appropriate configuration (through any terminal session):

```bash
nginx -c nginx.conf
```



For the frontend, run the following commands:

```bash
cd frontend
yarn build
yarn start
```

This will start a Node.js server on port 3000.

For the backend, run the following command:

```bash
cd backend
export DB_URL='postgresql://user:your_desired_password@localhost/sport_hours'
pipenv run python3.7 run.py
```

This will start a Python server on port 5000.

You're done! Visit `localhost` on port 80 to see the application in action.