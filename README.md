# eMenu - Python, Django, Docker, REST Api

## Project uses 
- **Django** - as web framework with ORM functionality
- **Django REST Framework** - to facilitate creation of REST Api; also provides Serialization to JSON; generation of Schema
- **django-filters** - to facilitate Filtering in DRF
- **Celery** - to implement execution of scheduled daily tasks (sending emails)
- **docker** - a complete container solution
- **httpie** - tool to interact with REST Api (used by addData.py)

## Tests
Following tests have been implemented:
- Code for sending emails and generating their content (menuapi/tasks.py)
- API Service using DRF client for testing APIViews


*Views and Serialization have NOT been tested with unit-tests because they use ready-made solution from DRF
and therefor not much coding was required.*

**NOTE/TODO:**
Testing API REST service using tools provided with Django REST Framework has NOT been COMPLETELY successful because of an issue present within the source code of DRF. 
*More investigation required.*

## Config 
Configuration of database is located  in **.env** file and **Docker-config** files

## Sample data:
A script **addData.py** has been created to add data to database (using API).
It can be used once the service is running.
it works as follows:
```
python addData.py [ meals <number_of_meals> ] [ menus <number_of_menus> <maximum_number_of_meals> ] -l <login:passwd>
```

## Install and run
A Script install.sh has been provided to facilitate building and running the project
	
## Performance
During "stress test" performed on the localhost (using **stressTest.py** script) the API Service served 100 requests in 15 seconds (10 req / 1.5 sec). This seems to be rather low performance and most possibly could be improved somehow.
	

	
