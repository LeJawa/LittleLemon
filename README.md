# Little Lemon website
Capstone project for the Meta Back-End Developer Professional Certificate on Coursera.

## Get started
In the terminal or command line, run `pipenv shell` followed by `pipenv install` to install the necessary dependencies.

Go into the `littlelemon` folder and run `python manage.py runserver`.

To access the API Demo, go to ![127.0.0.1:8000/](127.0.0.1:8000/) and follow the instructions.

You can also run the test suite by executing `python manage.py test`.

## Available APIs

Once the server is running, you can access the following endpoints. 

The ![API Demo](127.0.0.1:8000/) explains what can be accessed with each endpoint and what authentication is required to do so.
- `/restaurant/show/menu-items`
- `/restaurant/show/menu-items/<int:pk>`
- `/restaurant/manage/menu-items`
- `/restaurant/manage/menu-items/<int:pk>`
- `/restaurant/user/reservation/tables`
- `/restaurant/user/reservation/tables/<int:pk>`
- `/restaurant/staff/reservation/tables`
- `/restaurant/staff/reservation/tables/<int:pk>`

- The standard djoser authentication endpoints


