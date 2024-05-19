import oracledb
import json

conn = oracledb.connect(
        user="system",
        password="anish", #ENTER YOUR PASSWORD HERE!
        host="localhost",
        port="1521",
        service_name="XE"
    )

curr = conn.cursor()

try:
    #REMOVE THE QUOTES OVER THE BELOW STRING IF TABLES ARE ALREADY CREATED AND YOU'RE RUNNING THE SCRIPT FOR THE SECOND TIME>
    drop_tab_query = """
    DROP TABLE airplanes
    """

    curr.execute(drop_tab_query)

    drop_tab_query = """
    DROP TABLE models
    """
    curr.execute(drop_tab_query)

    drop_tab_query = """
    DROP TABLE technicians
    """
    curr.execute(drop_tab_query)


    drop_tab_query = """
    DROP TABLE expertise
    """
    curr.execute(drop_tab_query)

    drop_tab_query = """
    DROP TABLE tests
    """
    curr.execute(drop_tab_query)
except Exception as e:
    print (e)

create_airplaneTab_query = """
CREATE TABLE airplanes(
    registration_num CHAR(10) NOT NULL,
    model_num CHAR(5) NOT NULL,
    airline VARCHAR(50) NOT NULL
)
"""
curr.execute(create_airplaneTab_query)

create_modelTab_query = """
CREATE TABLE models(
    model_num CHAR(5) NOT NULL,
    capacity INT NOT NULL,
    weight INT NOT NULL
)
"""

curr.execute(create_modelTab_query)

create_technicianTab_query = """
CREATE TABLE technicians(
    ssn VARCHAR(11) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone_num VARCHAR(12) NOT NULL,
    street_address VARCHAR(200) NOT NULL,
    city VARCHAR(30) NOT NULL,
    country VARCHAR(50) NOT NULL,
    salary FLOAT NOT NULL
)
"""

curr.execute(create_technicianTab_query)

create_expertiseTab_query = """
CREATE TABLE expertise(
    model_num CHAR(5) NOT NULL,
    ssn VARCHAR(11) NOT NULL
)
"""

curr.execute(create_expertiseTab_query)

create_testTab_query = """
CREATE TABLE tests(
    test_num VARCHAR(8) NOT NULL,
    test_name VARCHAR(30) NOT NULL,
    ssn VARCHAR(11) NOT NULL,
    registration_num CHAR(10) NOT NULL,
    test_date DATE NOT NULL,
    maximum_score INT NOT NULL,
    number_of_hours INT NOT NULL,
    airplane_score INT NOT NULL
)
"""

curr.execute(create_testTab_query)

with open(r"dbms_import\current-gen-data\airplanes.json","r") as readFile:
    airplaneData = json.load(readFile)

counter = 0
for record in airplaneData:
    reg_num = record["registration_num"]
    
    model_num = record["model_num"]
    airline = record["airline"]

    insert_rec_query = f"INSERT INTO airplanes VALUES ('{reg_num}','{model_num}','{airline}')"
    print(insert_rec_query)
    counter+=1
    print("AIRPLANES", counter, "AIRPLANES")
    curr.execute(insert_rec_query)

with open(r"dbms_import\current-gen-data\plane_models.json","r") as readFile:
    modelData = json.load(readFile)


counter = 0
for record in modelData:
    model_num = record["model_num"]
    
    capacity = record["capacity"]
    weight = record["weight"]

    insert_rec_query = f"INSERT INTO models VALUES ('{model_num}','{capacity}','{weight}')"
    print(insert_rec_query)
    counter+=1
    print("MODELS", counter, "MODELS")
    curr.execute(insert_rec_query)

with open(r"dbms_import\current-gen-data\technicians.json","r") as readFile:
    technicianData = json.load(readFile)

counter = 0
for record in technicianData:
    ssn = record["ssn"]
    first_name = record["first_name"]
    last_name = record["last_name"]

    if "'" in last_name:
        last_name = ' '.join(last_name.split("'"))

    if "'" in first_name:
        first_name = ' '.join(first_name.split("'"))

    gender = record["gender"]

    if gender not in ["Male","Female","Agender"]:
        gender = "Agender"

    phone_num = record["phone_num"]
    street_address = record["street_address"]
    city = record["city"]
    country = record["country"]
    salary = record["salary"]

    if "'" in city:
        city = ' '.join(city.split("'"))

    insert_rec_query = f"INSERT INTO technicians VALUES ('{ssn}','{first_name}','{last_name}','{gender}','{phone_num}','{street_address}','{city}','{country}','{salary}')"
    print(insert_rec_query)
    counter+=1
    print("TECHNICIANS", counter, "TECHNICIANS")
    curr.execute(insert_rec_query)


with open(r"dbms_import\current-gen-data\expertise_data.json","r") as readFile:
    expertiseData = json.load(readFile)

counter = 0
for record in expertiseData:
    model_num = record["model_num"]
    ssn = record["ssn"]

    insert_rec_query = f"INSERT INTO expertise VALUES ('{model_num}','{ssn}')"
    print(insert_rec_query)
    counter+=1
    print("EXPERTISE", counter, "EXPERTISE")
    curr.execute(insert_rec_query)


with open(r"dbms_import\current-gen-data\tests.json","r") as readFile:
    testData = json.load(readFile)

counter = 0
for record in testData:
    test_num = record["test_num"]
    test_name = record["test_name"]
    ssn = record["ssn"]
    registration_num = record["registration_num"]
    test_date = record["date"]
    maximum_score = record["maximum_score"]
    number_of_hours = record["number_of_hours"]
    airplane_score = record["airplane_score"]

    insert_rec_query = f"INSERT INTO tests VALUES ('{test_num}','{test_name}','{ssn}','{registration_num}',TO_DATE('{test_date}','YYYY-MM-DD'),'{maximum_score}','{number_of_hours}','{airplane_score}')"
    print(insert_rec_query)
    counter+=1
    print("TESTS", counter, "TESTS")
    curr.execute(insert_rec_query)

curr.execute("COMMIT")


print("SUCCESSFUL!")