import requests
import collections
import json

headerHTTP = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                        'image/webp,/;q=0.8',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 '
                            'Firefox/93.0'}
id = 0
employee_name = ""
employee_salary = 0
profile_image = ""


def select_a_function():
    global id
    id = 0
    global employee_name
    employee_name = 0
    global employee_salary
    employee_salary = 0
    global profile_image
    profile_image = 0
    while True:
        try:
            print("What would you like to do?")
            print("1.Update Employee")
            print("2.Delete Employee")
            print("3.Create Employee")
            print("4.List all Employee")
            print("5.Show detail Employee")
            print("6.Average salary Employee")
            print("7.Age info Employee\n")

            selection = int(input("Enter a number from 1-7:\n"))
            if selection == 1 or selection == 2 or selection == 3:
                if selection == 1 or selection == 2:
                    id_emp = input("\nEnter an id:\n")
                if selection == 1 or selection == 3:
                    employee_name = input("\nEnter an Employee Name:\n")
                    employee_salary = input("Enter an Employee Salary:\n")
                    employee_age = input("Enter an Employee Age:\n")
                if selection == 1:
                    profile_image = input("Enter a Profile Picture:\n")
                if selection == 1:
                    print(update_employee(id_emp, employee_name, employee_salary, employee_age, profile_image))
                elif selection == 2:
                    response = delete_employee(id_emp)
                    if response != {}:
                        print("Employee #" + response['data'] + " " + response['message'])
                    else:
                        print("Deletion canceled")
                elif selection == 3:
                    print(create_employee(employee_name, employee_salary, employee_age))

            if selection == 4:

                list_all = get_all_employee()
                if list_all is None:
                    continue
                    print(list_all)
                for i in range(len(list_all)):
                    if i % 10 == 0 and i > 0:
                        input("Press enter to continue")
                    print(str(i + 1) + "|Employee " + list_all[i]['employee_name'])
            if selection == 5:
                emp_id = input("Enter employee id")
                employee = show_employee_detail(emp_id)
                print("Salary: " + str(employee['employee_salary']))
                print("Age: " + str(employee['employee_age']))
                print("Employee Name: " + employee['employee_name'])
            if selection == 6:
                print("Average of all salaries: " + str(show_avg_salary()))
            if selection == 7:
                mini = input("Enter min age:\n")
                maxi = input("Enter max age:\n")
                avg = age_info(mini, maxi)
                print("Lowest salary for this age range: " + str(avg['lowest']))
                print("Highest salary for this age range: " + str(avg['highest']))
                print("Average salary for this age range : " + str(avg['average']))
        # except ValueError:
        #     print("Enter something a number")
        except json.decoder.JSONDecodeError:
            print("Response is empty, try again later")


def update_employee(id: int, employee_name: str, employee_salary: int, employee_age: int, profile_image: str):
    response = requests.put('https://dummy.restapiexample.com/api/v1/update/' + str(id),
                            data={'employee_name': employee_name,
                                  'employee_salary': employee_salary,
                                  'employee_age': employee_age,
                                  'profile_image': profile_image}, headers=headerHTTP)
    return response.json()['data']


def delete_employee(id: int):  # done
    response_test = show_employee_detail(id)
    confirmation = input("Delete Employee " + response_test['employee_name'] + "? (Y/N)")
    if "Y" in confirmation.upper():
        response = requests.delete('https://dummy.restapiexample.com/api/v1/delete/' + str(id), headers=headerHTTP)
        return response.json()
    else:
        return {}


def create_employee(employee_name: str, employee_salary: int, employee_age: int):
    response = requests.post('https://dummy.restapiexample.com/api/v1/create',
                             data={'employee_name': employee_name,
                                   'employee_salary': employee_salary,
                                   'employee_age': employee_age}, headers=headerHTTP)
    return response.json()["data"]


def get_all_employee():  # done
    response = requests.get('https://dummy.restapiexample.com/api/v1/employees', headers=headerHTTP)
    return response.json()["data"]


def show_employee_detail(id: int):  # done
    response = requests.get('https://dummy.restapiexample.com/api/v1/employee/' + str(id), headers=headerHTTP)
    return response.json()["data"]


def show_avg_salary():
    response = requests.get('https://dummy.restapiexample.com/api/v1/employees', headers=headerHTTP)
    total = 0
    list = response.json()["data"]
    for i in list:
        total += i['employee_salary']
    return total / len(list)


def age_info(start: int, end: int):  # done
    try:
        response = requests.get('https://dummy.restapiexample.com/api/v1/employees',
                                headers=headerHTTP)
        tot_avg = 0
        lowest = -1
        highest = -1
        responseObject = response.json()["data"]
        # newlist = sorted(list_to_be_sorted, key=lambda d: d['name'])
        list_emp = sorted(responseObject, key=lambda k: k['employee_age'])
        for i in range(len(list_emp)):
            if int(start) <= list_emp[i]['employee_age'] <= int(end):
                if list_emp[i]['employee_age'] >= int(start) and int(lowest) == -1:
                    lowest = list_emp[i]['employee_salary']
                if list_emp[-i]['employee_age'] <= int(end) and int(highest) == -1:
                    print(list_emp[-i])
                    highest = list_emp[-i]['employee_salary']
                tot_avg += list_emp[i]['employee_salary']
        if lowest == -1:
            lowest = list_emp[0]['employee_salary']
        if highest == -1:
            highest = list_emp[len(list_emp) - 1]['employee_salary']
    except json.decoder.JSONDecodeError as err:
        print("Response is empty, try again later")

    return {'highest': highest, 'lowest': lowest, 'average': tot_avg / len(list(range(int(start), int(end))))}


select_a_function()
