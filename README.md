# MySQL App

## How to Use it

### 1. Generate Fake Data
Run the `application_file_generator.py` program to generate fake data:
```
python3 application_file_generator.py
```
The data will be saved in the ./applications/ folder. 

### 2. Set MySQL Connection Details
Store your MySQL connection details - host, username, and password - in environment variables.
``` 
export HOST={your host}
export USER={your user - usually root}
export PASSWORD={your password}
```

### 3. Insert Data into MySQL
To insert rows into the existing table without cleaning it, run:
```commandline
python3 main.py -c 'False'
```
or
```commandline
python3 main.py --clean_table 'False'
```

To clean the table before adding new rows, run:
```commandline
python3 main.py
```
or 
```commandline
python3 main.py -c 'True'
```
or
```commandline
python3 main.py --clean_table 'True'
```