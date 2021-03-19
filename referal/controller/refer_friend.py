import json

from common.com import *
from common.json_response import *
from referal.serializers import ReferalSerializer

SECTOR = ['GOVERNMENT', 'PRIVATE']
SALARY_BUDGET = ['0 - 2 Lakh per anum', '2 - 5 Lakh per anum', '5 - 10 Lakh per anum', '10 - 20 Lakh per anum',
                 '>20 Lakh per anum']
JOB_TYPE = ['PART TIME', 'FULL TIME']
EXPERIENCE_LEVEL = ['0 - 2 YEARS', '2 - 5 YEARS', '5 - 10 YEARS', '10 - 15 YEARS', '15+ YEARS']
EXPERIENCE_PERIOD = ['DAY', 'MONTH', 'YEAR']


class ReferFriendHelper:
    def __init__(self, request):
        self.request = request

        if request.method == 'GET':
            self.input_data = request.GET.dict()
        else:
            self.input_data = request.data

    def post(self):
        if not self.input_data:
            return {'message': 'Error! data is missing.', 'data': {}, 'status': False}, BadRequest
        if 'first_name' not in self.input_data or not self.input_data['first_name']:
            return {'message': 'Error! First Name is missing.', 'data': {}, 'status': False}, BadRequest
        if 'email' not in self.input_data or not self.input_data['email']:
            return {'message': 'Error! email is missing.', 'data': {}, 'status': False}, BadRequest
        if 'phone_number' not in self.input_data or not self.input_data['phone_number']:
            return {'message': 'Error! phone_number is missing.', 'data': {}, 'status': False}, BadRequest
        if 'company' not in self.input_data or not self.input_data['company']:
            return {'message': 'Error! company is missing.', 'data': {}, 'status': False}, BadRequest
        if 'job_type' not in self.input_data or not self.input_data['job_type']:
            return {'message': 'Error! job_type is missing.', 'data': {}, 'status': False}, BadRequest
        if 'job_title' not in self.input_data or not self.input_data['job_title']:
            return {'message': 'Error! job_title is missing.', 'data': {}, 'status': False}, BadRequest
        if 'job_location' not in self.input_data or not self.input_data['job_location']:
            return {'message': 'Error! job_location is missing.', 'data': {}, 'status': False}, BadRequest
        if 'roles_and_responsiblities' not in self.input_data or not self.input_data['roles_and_responsiblities']:
            return {'message': 'Error! roles_and_responsiblities is missing.', 'data': {}, 'status': False}, BadRequest

        if self.input_data['job_type'] not in JOB_TYPE:
            return {'message': f'Error! invalid job_type, job_type should be one of {", ".join(JOB_TYPE)}', 'data': {},
                    'status': False}, BadRequest

        try:
            slz = ReferalSerializer(data=self.input_data)
            if slz.is_valid():
                slz.save()
            else:
                return {'message': 'Error! ' + str(slz.errors), 'data': {}, 'status': False}, BadRequest
        except Exception as e:
            return {'message': 'Error! ' + str(e), 'data': {}, 'status': False}, BadRequest
        return {'message': 'Success! Your request is successfully submitted.', 'data': {}, 'status': True}, OK
