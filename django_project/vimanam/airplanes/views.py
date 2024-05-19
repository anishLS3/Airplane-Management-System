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
                '1':"registration_num",
                '2':"model_num",
                '3':"airline"
            }

            search_query = f"SELECT * FROM airplanes WHERE {fields_map[field_param]} LIKE '%{search_param}%'"
            data = curr.execute(search_query)
        else:
            gen_query = "SELECT * FROM airplanes"
            data = curr.execute(gen_query)

        context = []

        for record in data:
            context_item = {
                "registration_num":record[0],
                "model_num":record[1],
                "airline":record[2],
            }
            context.append(context_item)

    return render(request, 'airplanes.html', {"context":context})

def get_airplane_data(request, reg_num):
    conn = oracledb.connect(
        user="system",
        password="anish",
        host="localhost",
        port="1521",
        service_name="XE"
    )

    print(reg_num)

    curr = conn.cursor()

    query = f"SELECT * FROM airplanes WHERE registration_num = {reg_num}"

    result = curr.execute(query)

    context = None

    for record in result:
        airplane_details = {
            "registration_num":record[0],
            "model_num":record[1],
            "airline":record[2],
        }

    tests_query = f"""
        SELECT * FROM tests
        WHERE registration_num = {reg_num}
        ORDER BY test_date DESC
    """

    result = curr.execute(tests_query)

    tests_details = []

    counter = 1
    for record in result:
        test_item = {
            "serial_num": counter,
            "test_num":record[0],
            "test_name":record[1],
            "ssn":record[2],
            "registration_num": record[3],
            "test_date": record[4].date().__str__(),
            "maximum_score": record[5],
            "number_of_hours": record[6],
            "airplane_score": record[7],
        }
        tests_details.append(test_item)
        counter += 1

    model_query = f"""
        SELECT models.model_num, models.capacity, models.weight
        FROM models
        WHERE model_num = (
            SELECT model_num FROM airplanes
            WHERE registration_num = {reg_num}
        )
    """ 

    result = curr.execute(model_query)

    for record in result:
        model_details = {
                "model_num":record[0],
                "capacity":record[1],
                "weight":record[2],
        }

    
    technician_query = f"""
        SELECT ssn, first_name, last_name
        FROM technicians
        WHERE ssn IN (
            SELECT ssn 
            FROM expertise
            WHERE model_num = '{model_details["model_num"]}'
        )
    """
    result = curr.execute(technician_query)

    technicians_details = []

    for record in result:
        technician_item = {
            "ssn": record[0],
            "first_name":record[1],
            "last_name":record[2],
        }
        technicians_details.append(technician_item)

    print(technicians_details)
    
    context = {
        "airplane_details":airplane_details,
        "tests_details":tests_details,
        "model_details": model_details,
        "technicians_details": technicians_details
    }




    return render(request, 'airplaneProfile.html', {"context": context})    

    



