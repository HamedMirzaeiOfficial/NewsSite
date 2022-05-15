# NewsSite
a website for share news with people. This site was created with the aim of sharing news in different categories. It has features such as displaying news by category, search by content, comment system and communication with the admin.


## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/HamedMirzaeiOfficial/NewsSite.git
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000`.



