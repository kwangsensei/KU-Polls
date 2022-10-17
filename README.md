## Online Polls And Surveys For KU

![Unittest](https://github.com/KwangSensei/ku-polls/actions/workflows/test.yml/badge.svg) 
[![codecov](https://codecov.io/gh/KwangSensei/ku-polls/branch/master/graph/badge.svg?token=F5JIA3HDYY)](https://codecov.io/gh/KwangSensei/ku-polls)

An application for conducting online polls and surveys based 
on the [Django Tutorial project](https://docs.djangoproject.com/en/4.1/intro/tutorial01/), with additional features.

App created as part of the [Individual Software Process](https://cpske.github.io/ISP) course at Kasetsart University.

## How To Install

1. ```Python 3.9``` or higher is required.

2. Clone this GitHub repository. Or run this command:
```
git clone https://github.com/KwangSensei/ku-polls.git
```

3. Locate the file directory.

4. Change filename ```sample.env``` to ```.env``` and adjust values as the instruction say.

5. Run command below to create virtual environment.
```
# create the virtual env in "env/", only 1 time
python -m venv env

# start the virtual env in bash or zsh
. env\Scripts\activate
```

6. Run command below to install required packages.
```
pip install -r requirements.txt
```
## Running The App

1. Run migrations by fellow command:
```
python manage.py migrate
```

2. If you wish to use data from data fixtures, please run command:
```
python manage.py loaddata polls\data_fixtures\polls.json
```

3. Start the server by run:
```
python manage.py runserver
```

4. Then follow the link ```http://localhost:8000``` to web application.

5. To create ```admin``` account:
```
python manage.py createsuperuser

# enter your username, email, password and password confirmation, in this case
Username: admin
Email address: admin@example.com
Password: **********
Password (again): *********
Superuser created successfully.
```

- *Note: You can create new users, questions and choices in /admin page.*

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project%20Plan)
- [Iteration 1 Plan](../../wiki/Iteration%201%20Plan) and [Task Board](https://github.com/users/KwangSensei/projects/1/views/16)
- [Iteration 2 Plan](../../wiki/Iteration%202%20Plan) and [Task Board](https://github.com/users/KwangSensei/projects/1/views/13)
- [Iteration 3 Plan](../../wiki/Iteration%203%20Plan) and [Task Board](https://github.com/users/KwangSensei/projects/1/views/18)
- [Iteration 4 Plan](../../wiki/Iteration%204%20Plan) and [Task Board](https://github.com/users/KwangSensei/projects/1/views/19)
