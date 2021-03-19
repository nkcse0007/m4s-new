import uuid
import requests
from common.json_response import *
from common.jwt_security import *
import string
import random
from django.core.files.storage import FileSystemStorage
from dateutil.parser import parse
import pandas as pd

ZONES = ['North 1', 'North 2', 'North 3', 'North 4', 'East 1', 'East 2', 'East 3', 'East 4', 'South 1',
         'South 2', 'South 3', 'South 4', 'West 1', 'West 2', 'West 3', 'West 4']
INDIAN_STATES = ["Andhra Pradesh",
                 "Arunachal Pradesh",
                 "Assam",
                 "Bihar",
                 "Chhattisgarh",
                 "Goa",
                 "Gujarat",
                 "Haryana",
                 "Himachal Pradesh",
                 "Jammu and Kashmir",
                 "Jharkhand",
                 "Karnataka",
                 "Kerala",
                 "Madhya Pradesh",
                 "Maharashtra",
                 "Manipur",
                 "Meghalaya",
                 "Mizoram",
                 "Nagaland",
                 "Odisha",
                 "Punjab",
                 "Rajasthan",
                 "Sikkim",
                 "Tamil Nadu",
                 "Telangana",
                 "Tripura",
                 "Uttarakhand",
                 "Uttar Pradesh",
                 "West Bengal",
                 "Andaman and Nicobar Islands",
                 "Chandigarh",
                 "Dadra and Nagar Haveli",
                 "Daman and Diu",
                 "Delhi",
                 "Lakshadweep",
                 "Puducherry"]


def change_file_name(filename):
    extension = filename.split('.')[-1]
    return uuid.uuid4().hex + '.' + extension


def save_files_to_filesystem(file_name, file):
    fs = FileSystemStorage()
    filename = fs.save('sheets/' + file_name, file)
    uploaded_file_url = fs.url(filename)
    return uploaded_file_url


def get_client_ip(request):
    x_forwarded_for = request.remote_addr
    ip = x_forwarded_for.split(',')[0]
    return ip


# TODO get location from ip
def get_location(ip):
    try:
        loc = requests.request("GET", "http://ip-api.com/json/{0}".format(ip)).json()
        print(loc)
        location = loc['city'] + ', ' + loc['country'] + ', ' + loc['countryCode']
    except Exception as e:
        print(e)
        location = "unidentified"

    return location


def get_user_from_token(request):
    token = get_token(request)
    Jwt = JwtAuth(token)
    user_id, headers = Jwt.decode()[0]['userId'] if 'userId' in Jwt.decode()[0] else 0, Jwt.decode()[1]
    return user_id


def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def alpha_id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def validate_data(sheet_errors, i, sheet_data):
    try:
        if not sheet_data['Client Name'][i].replace(' ', '').replace('(', '').replace(')', '').replace('.',
                                                                                                       '').isalpha():
            sheet_errors.append({
                'message': 'Client Name is not completely alphabet',
                'value': sheet_data['Client Name'][i],
                'row_number': i + 1
            })
    except:
        pass
    # For "Project Code" No need any validation
    try:
        start_date = parse(str(sheet_data['Exam Start Date'][i]))
        try:
            end_date = parse(str(sheet_data['Exam End Date'][i]))
            if end_date < start_date:
                sheet_errors.append({
                    'message': 'Exam End Date should be greater then or equals to Exam Start Date',
                    'value': sheet_data['Exam End Date'][i],
                    'row_number': i + 1
                })
        except:
            sheet_errors.append({
                'message': 'Invalid Exam End Date',
                'value': sheet_data['Exam End Date'][i],
                'row_number': i + 1
            })
    except:
        sheet_errors.append({
            'message': 'Invalid Exam Start Date',
            'value': sheet_data['Exam Start Date'][i],
            'row_number': i + 1
        })
    if pd.isna(sheet_data['SSC Region'][i]):
        pass
    else:
        if not sheet_data['SSC Region'][i].replace(' ', '').replace('(', '').replace(')', '').replace('.',
                                                                                                      '').isalpha():
            sheet_errors.append({
                'message': 'SSC Region is not completely alphabet',
                'value': sheet_data['SSC Region'][i],
                'row_number': i + 1
            })

    if sheet_data['Zone'][i] not in ZONES:
        sheet_errors.append({
            'message': 'Zone should be one of ' + ', '.join(ZONES),
            'value': sheet_data['Zone'][i],
            'row_number': i + 1
        })

    if sheet_data['State'][i].title() not in INDIAN_STATES:
        sheet_errors.append({
            'message': 'Not an indian state',
            'value': sheet_data['State'][i],
            'row_number': i + 1
        })

    if not sheet_data['City'][i].replace(' ', '').replace('(', '').replace(')', '').replace('.', '').isalpha():
        sheet_errors.append({
            'message': 'City is not completely alphabet',
            'value': sheet_data['City'][i],
            'row_number': i + 1
        })

    try:
        code = int(sheet_data['Venue Code'][i])
    except:
        sheet_errors.append({
            'message': 'Venue Code should be an integer',
            'value': sheet_data['Venue Code'][i],
            'row_number': i + 1
        })
    # For "Venue Name" No need any validation
    # For "Address" No need any validation
    try:
        code = int(sheet_data['Pincode'][i])
        if len(str(sheet_data['Pincode'][i])) != 6:
            sheet_errors.append({
                'message': 'Pincode should be of length 6',
                'value': sheet_data['Pincode'][i],
                'row_number': i + 1
            })
    except:
        sheet_errors.append({
            'message': 'Pincode should be an integer',
            'value': sheet_data['Pincode'][i],
            'row_number': i + 1
        })
    if not sheet_data['Center Contact Name'][i].replace(' ', '').replace('(', '').replace(')', '').replace('.',
                                                                                                           '').isalpha():
        sheet_errors.append({
            'message': 'Center Contact Name is not completely alphabet',
            'value': sheet_data['Center Contact Name'][i],
            'row_number': i + 1
        })
    try:
        val = int(sheet_data['Center Contact Number'][i])
    except:
        sheet_errors.append({
            'message': 'Center Contact Number should be an integer',
            'value': sheet_data['Center Contact Number'][i],
            'row_number': i + 1
        })
    try:
        exam_date = parse(str(sheet_data['Exam Date'][i]))
        try:
            if not start_date <= exam_date <= end_date:
                sheet_errors.append({
                    'message': 'Exam End Date should be greater then or equals to Exam Start Date',
                    'value': sheet_data['Exam End Date'][i],
                    'row_number': i + 1
                })
        except:
            sheet_errors.append({
                'message': 'Invalid Exam Date due to invalid Exam Start Date or invalid Exam End Date',
                'value': sheet_data['Exam Date'][i],
                'row_number': i + 1
            })
    except:
        sheet_errors.append({
            'message': 'Invalid Exam Date',
            'value': sheet_data['Exam Date'][i],
            'row_number': i + 1
        })
    try:
        val = int(sheet_data['Shift 1'][i])
    except:
        sheet_errors.append({
            'message': 'Shift 1 should not be an integer',
            'value': sheet_data['Shift 1'][i],
            'row_number': i + 1
        })
    try:
        timeformat = "%I:%M %p"
        sheet_data['Shift 1 timings'][i].strftime(timeformat)
    except:
        sheet_errors.append({
            'message': 'Shift 1 timings is not valid, format should be 11:30 AM',
            'value': sheet_data['Shift 1 timings'][i],
            'row_number': i + 1
        })
    try:
        val = int(sheet_data['Shift 2'][i])
    except:
        sheet_errors.append({
            'message': 'Shift 2 should not be an integer',
            'value': sheet_data['Shift 2'][i],
            'row_number': i + 1
        })
    try:
        timeformat = "%I:%M %p"
        sheet_data['Shift 2 timings'][i].strftime(timeformat)
    except:
        sheet_errors.append({
            'message': 'Shift 2 timings is not valid, format should be 11:30 AM',
            'value': sheet_data['Shift 2 timings'][i],
            'row_number': i + 1
        })
    try:
        val = int(sheet_data['Shift 3'][i])
    except:
        sheet_errors.append({
            'message': 'Shift 3 should not be an integer',
            'value': sheet_data['Shift 3'][i],
            'row_number': i + 1
        })
    try:
        timeformat = "%I:%M %p"
        sheet_data['Shift 3 timings'][i].strftime(timeformat)
    except:
        sheet_errors.append({
            'message': 'Shift 3 timings is not valid, format should be 11:30 AM',
            'value': sheet_data['Shift 3 timings'][i],
            'row_number': i + 1
        })
    try:
        val = int(sheet_data['Max Count'][i])
    except:
        sheet_errors.append({
            'message': 'Max Count should be an integer',
            'value': sheet_data['Max Count'][i],
            'row_number': i + 1
        })
    try:
        val = int(sheet_data['Total Count'][i])
    except:
        sheet_errors.append({
            'message': 'Total Count should be an integer',
            'value': sheet_data['Total Count'][i],
            'row_number': i + 1
        })
    return sheet_errors
