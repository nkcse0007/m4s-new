from common.com import *
from common.json_response import *
from common.jwt_security import *
from common.validations import *
import hashlib
import json
from authentication.models import User
from uuid import uuid4
from django.contrib.auth import authenticate


class Login:
    def __init__(self, request):
        self.request = request
        self.input_data = json.loads(request.body.decode('utf-8'))

    def post(self):
        if not self.input_data:
            return {'message': 'Error! data is missing.', 'data': {}, 'status': False}, BadRequest
        elif 'email' not in self.input_data or self.input_data['email'] == '':
            return {'message': 'Error! email is missing.', 'data': {}, 'status': False}, BadRequest
        elif 'password' not in self.input_data or self.input_data['password'] == '':
            return {'message': 'Error! password is missing.', 'data': {}, 'status': False}, BadRequest

        elif not User.objects.filter(email=self.input_data['email']).exists():
            return {'message': 'Error! You do not have any account.Please Register first.', 'data': {},
                    'status': False}, BadRequest
        else:
            user = authenticate(username=self.input_data['email'], password=self.input_data['password'])
            if user is None:
                return {'message': 'Error! Invalid email or password.', 'data': {},
                        'status': False}, BadRequest
            user = User.objects.filter(email=self.input_data['email']).values('name', 'email', 'phone', 'id',
                                                                                 'role').get()

            try:
                permissions = [pem['permissions__title'] for pem in
                               list(User.objects.filter(id=user['id']).values('permissions__title')) if
                               pem['permissions__title'] is not None]
            except:
                permissions = []
            Jwt = JwtAuth('MSI@22551')
            token = Jwt.encode(
                {'id': str(user['id']), 'email': user['email'], 'name': user['name'], 'permissions': permissions,
                 'role': user['role']}, self.request)
            user['permissions'] = permissions
            user['token'] = token
            return {'status': True,
                    'message': 'Login successful.',
                    'data': user}, OK
