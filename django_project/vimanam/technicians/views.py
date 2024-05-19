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
                '1':"ssn",
                '2':"first_name",
                '3':"last_name",
                '4':"gender",
                '5':"phone_num",
                '6':"street_address",
                '7':"city",
                '8':"country",
                '9':"salary"
            }

            search_query = f"SELECT * FROM technicians WHERE {fields_map[field_param]} LIKE '%{search_param}%'"
            data = curr.execute(search_query)
        else:
            gen_query = "SELECT * FROM technicians"
            data = curr.execute(gen_query)

        context = []

        for record in data:
            context_item = {
                "ssn":record[0],
                "first_name":record[1],
                "last_name":record[2],
                "gender": record[3],
                "phone_num": record[4],
                "street_address": record[5],
                "city": record[6],
                "country": record[7],
                "salary": record[8]
            }
            context.append(context_item)

    return render(request, 'technicians.html', {"context":context})

def get_technician_data(request, ssn):
    conn = oracledb.connect(
        user="system",
        password="anish",
        host="localhost",
        port="1521",
        service_name="XE"
    )

    curr = conn.cursor()

    query = f"SELECT * FROM technicians WHERE ssn = '{ssn}'"

    result = curr.execute(query)

    for record in result:
        technician_details = {
            "ssn":record[0],
            "first_name":record[1],
            "last_name":record[2],
            "gender": record[3],
            "phone_num": record[4],
            "street_address": record[5],
            "city": record[6],
            "country": record[7],
            "salary": record[8]
        }

    model_query = f"""
        SELECT * FROM models
        WHERE model_num IN (
            SELECT model_num FROM expertise
            WHERE ssn = '{technician_details["ssn"]}'
        )
    """

    result = curr.execute(model_query)

    model_details = []
    for record in result:
        model_item = {
            "model_num": record[0],
            "capacity": record[1],
            "weight": record[2]
        }
        model_details.append(model_item)

    tests_query = f"""
        SELECT tests.test_date, tests.test_num, tests.airplane_score, tests.maximum_score, tests.registration_num, airplanes.model_num
        FROM tests, airplanes
        WHERE tests.ssn = '{technician_details["ssn"]}'
            AND tests.registration_num = airplanes.registration_num
        ORDER BY tests.test_date DESC
    """

    result = curr.execute(tests_query)

    test_details = []
    counter = 1
    for record in result:
        test_item = {
            "serial_num": counter,
            "test_date":str(record[0].date()),
            "test_num":record[1],
            "airplane_score": record[2],
            "maximum_score": record[3],
            "registration_num": record[4],
            "model_num": record[5]
        }
        test_details.append(test_item)
        counter += 1

    print(tests_query)

    context = {
        "technician_details":technician_details,
        "model_details": model_details,
        "test_details":test_details
    }
    return render(request, 'technicianProfile.html', {"context": context})    

    



