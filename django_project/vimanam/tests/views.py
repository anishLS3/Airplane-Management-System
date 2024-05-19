from django.shortcuts import render
from django.http import HttpResponse
import oracledb
import datetime

def search_query(search_param, field_param):
    fields_map = {
                '1':"test_num",
                '2':"test_name",
                '3':"ssn",
                '4':"registration_num",
                '5':"test_date",
                '6':"maximum_score",
                '7':"number_of_hours",
                '8':"airplane_score"
            }

    return f"SELECT * FROM tests WHERE {fields_map[field_param]} LIKE '%{search_param}%'"

def general_query():
    return "SELECT * FROM tests"

def yearwise_query(year_param_list):

    counter = 0
    query = ""
    for year in year_param_list:
        if not counter:
            query = f"""
                SELECT * FROM tests
                WHERE EXTRACT(YEAR FROM test_date) = '{year}'
            """
        else:
            query += ' ' + f"""
                OR EXTRACT(YEAR FROM test_date) = '{year}'
            """
        counter += 1

    return query   

def scorewise_query(score_param, addParam=False):
    score_char = '<' if score_param == '0' else '>=' 
    
    if addParam == False:
        query = f"""
            SELECT * FROM tests
            WHERE (airplane_score/maximum_score)*100 {score_char} 75
        """
    else:
        query = ' ' + f"""
            AND (airplane_score/maximum_score)*100 {score_char} 75
        """

    return query

def timewise_query(time_param, addParam=False):
    time_char = '<' if time_param == '0' else '>='

    if addParam == False:
        query = f"""
            SELECT * FROM tests
            WHERE number_of_hours {time_char} 8
        """
    else:
        query = ' ' + f"""
            AND number_of_hours {time_char} 8
        """

    return query


# Create your views here.
def get_context_data(request):
    conn = oracledb.connect(
        user="system",
        password="anish",
        host="localhost",
        port="1521",
        service_name="XE"
    )

    curr = conn.cursor()
    
    if request.method == "GET":
        search_param = request.GET.get('s', None)
        field_param = request.GET.get('f', None)
        year_param_list = request.GET.getlist('y', None) 
        score_param = request.GET.get('sc', None)
        time_param = request.GET.get('t', None)

        if search_param is not None:
            print("yahoo")
            query = search_query(search_param=search_param, field_param=field_param)
        elif len(year_param_list) != 0: 
            query = yearwise_query(year_param_list=year_param_list)
            
            if score_param is not None:
                query += scorewise_query(score_param=score_param, addParam=True)
            if time_param is not None:
                query += timewise_query(time_param=time_param, addParam=True)

        elif score_param is not None:
            query = scorewise_query(score_param=score_param)

            if time_param is not None:
                query += timewise_query(time_param=time_param, addParam=True)

        elif time_param is not None:
            query = timewise_query(time_param=time_param)
        else:
            query = general_query()
            
        query += ' ' + f"""
            ORDER BY test_date DESC
        """

        print(query)
        data = curr.execute(query)
        test_details = []

        for record in data:
            context_item = {
                "test_num":record[0],
                "test_name":record[1],
                "ssn":record[2],
                "registration_num": record[3],
                "test_date": record[4].date(),
                "maximum_score": record[5],
                "number_of_hours": record[6],
                "airplane_score": record[7],
            }
            test_details.append(context_item)

    context = {
        "test_details": test_details,
        "num_details": len(test_details)
    }

    return render(request, 'tests.html', {"context":context})

def get_test_data(request, test_num):
    conn = oracledb.connect(
        user="system",
        password="anish",
        host="localhost",
        port="1521",
        service_name="XE"
    )

    curr = conn.cursor()

    query = f"SELECT * FROM tests WHERE test_num = '{test_num}'"

    result = curr.execute(query)

    for record in result:
        test_details = {
            "test_num":record[0],
            "test_name":record[1],
            "ssn":record[2],
            "registration_num": record[3],
            "test_date": record[4].date(),
            "maximum_score": record[5],
            "number_of_hours": record[6],
            "airplane_score": record[7],
            }

    technician_query = f"""
        SELECT first_name, last_name
        FROM technicians
        WHERE ssn = '{test_details["ssn"]}'
    """

    result = curr.execute(technician_query)

    for record in result:
        technician_name = {
            "first_name": record[0],
            "last_name": record[1]
        }

    flight_query = f"""
        SELECT registration_num, model_num, airline
        FROM airplanes
        WHERE registration_num = '{test_details["registration_num"]}'
    """

    result = curr.execute(flight_query)

    for record in result:
        flight_details = {
            "registration_num" : record[0],
            "model_num" : record[1],
            "airline" : record[2],
        }

    context = {
        "test_details": test_details,
        "technician_details":technician_name,
        "flight_details": flight_details
    }


    return render(request, 'testProfile.html', {"context": context})