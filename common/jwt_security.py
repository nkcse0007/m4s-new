# import os
# from boto3 import exceptions
# import jwt
# from common import json_response as js
# from datetime import datetime, timedelta
# from uuid import uuid4
# from django.http import JsonResponse
# import json
# from uuid import uuid4
# from authentication.models import MISUser, JwtToken
# from authentication.serializers import JwtTokenSerializer
#
#
# class JwtAuth:
#
#     def __init__(self, row_or_token):
#         self.data = row_or_token
#
#     def encode(self, payload, request):
#         payload['exp']: datetime.utcnow() + timedelta(days=7)
#         private_key = open('common/private.pem').read()
#         user = MISUser.objects.filter(email=payload['email']).values().get()
#         expires_in = int((datetime.now() + timedelta(days=30)).timestamp())
#         jwt_id = uuid4().hex
#         try:
#             origin = request.META['HTTP_ORIGIN'].split('//')[1]
#             print(request.META['HTTP_ORIGIN'].split('//')[1])
#         except:
#             print('EXCEPTION IN ORIGIN>>')
#             # print(e)
#             origin = ''
#
#         print("================================================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#         encoded_jwt = jwt.encode(
#             {'userId': payload['id'], 'role': payload['role'], 'permissions': ','.join(payload['permissions']) if payload['permissions'] else ''},
#             private_key, algorithm=os.environ.get('ALGORITHM'), headers={
#                 'exp': expires_in,
#                 'aud': origin,
#                 'sub': user['email'],
#                 'iss': os.environ.get('ISSUER'),
#                 'jwtId': jwt_id,
#                 'iat': int(datetime.now().timestamp())
#             })
#         slz = JwtTokenSerializer(data={
#             'user': payload['id'],
#             'jwtId': jwt_id,
#             'expiresIn': datetime.fromtimestamp(expires_in),
#         })
#         if slz.is_valid():
#             slz.save()
#         else:
#             print('JWT TOKEN ERROR ' + slz.errors)
#         return encoded_jwt
#
#     def decode(self):
#         public_key = open('common/public.pub').read()
#         decoded_jwt = jwt.decode(self.data, public_key, algorithms=os.environ.get('ALGORITHM'))
#         headers = jwt.get_unverified_header(self.data)
#         decoded_jwt['id'] = decoded_jwt['userId']
#         return decoded_jwt, headers
#
#
# def authenticate_login(fun):
#     def wrap(request, *args, **kwargs):
#         try:
#             try:
#                 try:
#                     try:
#                         token = request.META.get('HTTP_AUTHORIZATION').split()
#                     except:
#                         token = request.request.META.get('HTTP_AUTHORIZATION').split()
#                     if not token:
#                         token = request.GET['access_token']
#                         if not token:
#                             token = json.loads(request.body.decode('utf-8'))['access_token']
#                 except:
#                     try:
#                         token = request.GET['access_token']
#                         if not token:
#                             token = json.loads(request.body.decode('utf-8'))['access_token']
#                     except:
#                         token = json.loads(request.body.decode('utf-8'))['access_token']
#
#                 if not token:
#                     return JsonResponse({'message': 'Error! Unauthorised user.', 'data': {}, 'is_active': False, 'status': False},
#                                         status=js.Unauthorized)
#
#                 if len(token) == 1:
#                     msg = 'Invalid token header. No credentials provided.'
#                     raise exceptions.AuthenticationFailed(msg)
#                 # elif len(token) > 2:
#                 #     msg = 'Invalid token header'
#                 #     raise exceptions.AuthenticationFailed(msg)
#
#                 try:
#                     token = token[-1]
#                     if token == "null":
#                         msg = 'Null token not allowed'
#                         raise exceptions.AuthenticationFailed(msg)
#                 except UnicodeError:
#                     msg = 'Invalid token header. Token string should not contain invalid characters.'
#                     raise exceptions.AuthenticationFailed(msg)
#
#                 dec = JwtAuth(str(token))
#                 profile_id, headers = dec.decode()
#             except Exception as e:
#                 print(e)
#                 return JsonResponse({'message': 'Error! Unauthorised user', 'data': {}, 'is_active': False, 'status': False},
#                                     status=js.Unauthorized)
#             if MISUser.objects.filter(id=profile_id['id']).exists():
#
#                 if not MISUser.objects.filter(id=profile_id['id']).values().get()['status']:
#                     return JsonResponse(
#                         {'message': f'Error! User has been blocked. Please contact admin.',
#                          'is_active': False, 'data': {}, 'status': False},
#                         status=js.Unauthorized)
#                 # if MISUser.objects.filter(id=profile_id['id']).values().get()['is_deleted']:
#                 #     return JsonResponse(
#                 #         {
#                 #             'message': 'Unauthorised',
#                 #             'is_active': False, 'status': False},
#                 #         status=js.Unauthorized)
#
#                 if not MISUser.objects.filter(id=profile_id['id']).values().exists():
#                     return JsonResponse(
#                         {
#                             'message': 'Error! Unauthorised', 'data': {},
#                             'is_active': False, 'status': False},
#                         status=js.Unauthorized)
#
#                 else:
#                     if JwtToken.objects.filter(jwtId=headers['jwtId']).values().last()[
#                         'expiresIn'].date() < datetime.now().date():
#                         return JsonResponse(
#                             {
#                                 'message': f'Error! Your session is expired. please login again.', 'data': {},
#                                 'is_active': False, 'status': False},
#                             status=js.Unauthorized)
#                 return fun(request, *args, **kwargs)
#
#             else:
#                 return JsonResponse({'message': 'Error! Unauthorised user.', 'data': {}, 'is_active': False, 'status': False},
#                                     status=js.Unauthorized)
#
#         except Exception as e:
#             return JsonResponse({'message': 'Error! authentication failed, Invalid token. Please login again.', 'data': {}, 'status': False}, status=js.Unauthorized)
#
#     return wrap
#
#
# def get_token(request):
#     try:
#         try:
#             token = request.META.get('HTTP_AUTHORIZATION').split()
#         except:
#             token = request.request.META.get('HTTP_AUTHORIZATION').split()
#         if not token:
#             token = request.GET['access_token']
#             if not token:
#                 token = json.loads(request.body.decode('utf-8'))['access_token']
#     except:
#         try:
#             token = request.GET['access_token']
#             if not token:
#                 token = json.loads(request.body.decode('utf-8'))['access_token']
#         except:
#             token = json.loads(request.body.decode('utf-8'))['access_token']
#
#     if not token:
#         return JsonResponse({'message': 'Error! Unauthorised user.', 'data': {}, 'is_active': False, 'status': False},
#                             status=js.Unauthorized)
#     return token[-1]
