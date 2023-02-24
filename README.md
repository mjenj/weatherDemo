# weatherDemo
Provide temprature data from an entered address


Requirements to run:

- Python3
- MySQL 8
- Django 2.2.28
- `pip3 install requests`
- `pip3 install mysql-connector`

Once downloaded run `python3 manage.py runserver` in 1 terminal \n
Make sure the MySQL db is running with `mysql.server start`

Credentials have been removed from the views.py file
- mapboxAPIKey requires a MapBox account. Create one here https://account.mapbox.com/
- "https://api.meteomatics.com/" requires a username and password. You need an account here as well


Improvements I'd like to make with more time:
- Restructure the code to take logic out of the `views.py` file
- Improve the UI
- Add pagination to history
- Add breadcrumbs to the UI
- Implement a better API secret scheme
- Add Unit tests
- Improve error handling

https://user-images.githubusercontent.com/18076764/221159968-bda40dcd-6fab-416d-ae4c-c2db6edd4399.mov

