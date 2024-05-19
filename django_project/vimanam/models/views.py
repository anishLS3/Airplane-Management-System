from django.shortcuts import render
from django.http import HttpResponse
import oracledb


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

        if search_param is not None:
            fields_map = {
                '1':"model_num",
                '2':"capacity",
                '3':"weight"
            }

            search_query = f"SELECT * FROM models WHERE {fields_map[field_param]} LIKE '%{search_param}%'"
            data = curr.execute(search_query)
        else:
            gen_query = "SELECT * FROM models"
            data = curr.execute(gen_query)

        context = []

        for record in data:
            context_item = {
                "model_num":record[0],
                "capacity":record[1],
                "weight":record[2],
            }
            context.append(context_item)

    return render(request, 'models.html', {"context":context})

def get_model_data(request, model_num):
    conn = oracledb.connect(
        user="system",
        password="anish",
        host="localhost",
        port="1521",
        service_name="XE"
    )

    curr = conn.cursor()
    print(model_num)
    query = f"SELECT * FROM models WHERE model_num = '{model_num}'"
    print(query)
    result = curr.execute(query)

    for record in result:
        model_details = {
            "model_num":record[0],
            "capacity":record[1],
            "weight":record[2],
        }

    airplanes_query = f"""
        SELECT registration_num, airline
        FROM airplanes
        WHERE model_num = '{model_details["model_num"]}'
    """

    result = curr.execute(airplanes_query)

    airplane_details = []
    counter = 1
    for record in result:
        airplane_item = {
            "serial_num": counter,
            "registration_num": record[0],
            "airline": record[1]
        }
        counter += 1
        airplane_details.append(airplane_item)

    technicians_query = f"""
        SELECT first_name, last_name, ssn
        FROM technicians
        WHERE ssn IN (
            SELECT ssn
            FROM expertise
            WHERE model_num = '{model_details["model_num"]}'
        )
    """

    result = curr.execute(technicians_query)

    technicians_details = []
    for record in result:
        technicians_item = {
            "first_name": record[0],
            "last_name": record[1],
            "ssn": record[2]
        }
        technicians_details.append(technicians_item)

    context = {
        "model_details":model_details,
        "airplane_details": airplane_details,
        "technicians_details": technicians_details
    }

    return render(request, 'modelProfile.html', {"context": context})    

    



