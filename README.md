# Rule_Engine
Project consists of two parts : 
	1) web section - 
		a) Provide user to insert new rule or update existing rule via form submission
		b) display user snippet of accepted data, rejected data(regex and rule rejected separately)
			. 
	2) Background process - 
		a) Parse entry_rule.json file to create entry_data json object
		b) Parse rule.json file to create rule_data json object
		c) For each data -
			. validate data if value is accordance with value_type or not. If invalidated redirect it to  
			  regex_validation_error file(acting as log file)
			. Apply rule if present in rule_data json object -
					if data is as per rule redirect it to database file 
					else redirect it to rule_validation_error file(acting as log file)
			. If no rule specified redirect it to database.
		d) Constraints used for defining rule - 
			. signal name is of type ATL followed by number [ATL[0-9]+]
			. value_type is one of Integer | String | Datetime
			. value for Integer type is in range format [[0-9]+-[0-9]+]
			. value for String type is only alphabet [[A-Za-z]]
			. value for Datetime is taken as current datetime by default.
		e) Constraints used for validating data - 
			. For string, only exact matching value is accpeted.
			. For Integer, value need to be within given range inclusive of boundary
			. For Datetime, value need not exceed rule specified datetime value
			

Installing :
	1) Used Visual studio code as text editor
	2) Install Anaconda3-5.2.0-Windows-x86_64
	3) Create virtual environment using conda create --name rule_parsing(env_name)
	4) Activate virtual environment using activate rule_parsing
	5) Install python 3.6.6 using pip install python=3.6.6
	6) Install django 2.1.1 using pip install Django=2.1.1
	7) Using anaconda prompt navigate to your desired folder where you want to copy this project(copy 
	   complete rule_engine folder)
	8) To run this project 
			python manage.py makemigrations	- create sql query
			python manage.py migrate - apply quey
			python manage.py createsuperuser - for admin interface
			python manage.py runserver - for running app. Use url to run on browser.
			http://127.0.0.1:8000/rule - for running app 
			http://127.0.0.1:8000/admin - for admin interface
	
	9) To run background process - Go to Background_process folder and run python rule_validation.py
