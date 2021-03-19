import json
import operator
from functools import reduce

from common.com import *
from common.json_response import *
from dateutil.parser import parse
from django.db.models import Q
from job.models import SubmitJob
from job.serializers import RequestTalentSerializer, SubmitJobSerializer, SubmitCVSerializer
from blogs.models import Blog
from cources.models import Course
from training.models import Training
import math

SECTOR = ['GOVERNMENT', 'PRIVATE']
SALARY_BUDGET = ['0 - 2 Lakh per anum', '2 - 5 Lakh per anum', '5 - 10 Lakh per anum', '10 - 20 Lakh per anum',
                 '>20 Lakh per anum']
JOB_TYPE = ['PART TIME', 'FULL TIME']
EXPERIENCE_LEVEL = ['0 - 2 YEARS', '2 - 5 YEARS', '5 - 10 YEARS', '10 - 15 YEARS', '15+ YEARS']
EXPERIENCE_PERIOD = ['DAY', 'MONTH', 'YEAR']


class RequestTalentHelper:
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
        if 'company' not in self.input_data or not self.input_data['company']:
            return {'message': 'Error! company is missing.', 'data': {}, 'status': False}, BadRequest
        if 'job_title' not in self.input_data or not self.input_data['job_title']:
            return {'message': 'Error! job_title is missing.', 'data': {}, 'status': False}, BadRequest
        if 'job_location' not in self.input_data or not self.input_data['job_location']:
            return {'message': 'Error! job_location is missing.', 'data': {}, 'status': False}, BadRequest
        if 'phone_number' not in self.input_data or not self.input_data['phone_number']:
            return {'message': 'Error! phone_number is missing.', 'data': {}, 'status': False}, BadRequest
        if 'help_text' not in self.input_data or not self.input_data['help_text']:
            return {'message': 'Error! help_text is missing.', 'data': {}, 'status': False}, BadRequest
        if 'experience_period' in self.input_data:
            if self.input_data['experience_period'] not in ['YEAR', 'MONTH', 'DAY']:
                return {
                           'message': 'Error! invalid experience_period, experience_period should be one of YEAR, MONTH, DAY',
                           'data': {}, 'status': False}, BadRequest
        try:
            if 'expected_joining_date' in self.input_data and self.input_data['expected_joining_date']:
                self.input_data['expected_joining_date'] = parse(self.input_data['expected_joining_date'])
            else:
                del self.input_data['expected_joining_date']
        except:
            del self.input_data['expected_joining_date']
        try:
            slz = RequestTalentSerializer(data=self.input_data)
            if slz.is_valid():
                slz.save()
            else:
                return {'message': 'Error! ' + str(slz.errors), 'data': {}, 'status': False}, BadRequest
        except Exception as e:
            return {'message': 'Error! ' + str(e), 'data': {}, 'status': False}, BadRequest
        return {'message': 'Success! Your request is successfully submitted.', 'data': {}, 'status': True}, OK


class SubmitJobHelper:
    def __init__(self, request):
        self.request = request

        if request.method == 'GET':
            self.input_data = request.GET.dict()
        else:
            self.input_data = request.data

    def get(self):
        if 'id' not in self.input_data:
            return {'message': 'Error! id is required.', 'data': {}, 'status': False}, BadRequest
        data = SubmitJob.objects.filter(id=self.input_data['id']).values().last()

        return {'message': '', 'data': data, 'status': True}, OK

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
        if 'experience_level' not in self.input_data or not self.input_data['experience_level']:
            return {'message': 'Error! experience_level is missing.', 'data': {}, 'status': False}, BadRequest
        if 'salary_budget' not in self.input_data or not self.input_data['salary_budget']:
            return {'message': 'Error! salary_budget is missing.', 'data': {}, 'status': False}, BadRequest
        if 'roles_and_responsiblities' not in self.input_data or not self.input_data['roles_and_responsiblities']:
            return {'message': 'Error! roles_and_responsiblities is missing.', 'data': {}, 'status': False}, BadRequest
        if 'remote_job' not in self.input_data:
            return {'message': 'Error! remote_job is missing.', 'data': {}, 'status': False}, BadRequest


        if self.input_data['job_type'] not in JOB_TYPE:
            return {'message': f'Error! invalid job_type, job_type should be one of {", ".join(JOB_TYPE)}', 'data': {},
                    'status': False}, BadRequest
        if self.input_data['sector'] not in SECTOR:
            return {'message': f'Error! invalid sector, sector should be one of {", ".join(SECTOR)}', 'data': {},
                    'status': False}, BadRequest
        if self.input_data['experience_level'] not in EXPERIENCE_LEVEL:
            return {
                       'message': f'Error! invalid experience_level, experience_level should be one of {", ".join(EXPERIENCE_LEVEL)}',
                       'data': {},
                       'status': False}, BadRequest
        if self.input_data['salary_budget'] not in SALARY_BUDGET:
            return {
                       'message': f'Error! invalid salary_budget, salary_budget should be one of {", ".join(SALARY_BUDGET)}',
                       'data': {},
                       'status': False}, BadRequest

        try:
            slz = SubmitJobSerializer(data=self.input_data)
            if slz.is_valid():
                slz.save()
            else:
                return {'message': 'Error! ' + str(slz.errors), 'data': {}, 'status': False}, BadRequest
        except Exception as e:
            return {'message': 'Error! ' + str(e), 'data': {}, 'status': False}, BadRequest
        return {'message': 'Success! Your job is successfully submitted.', 'data': {}, 'status': True}, OK


class SubmitCvHelper:
    def __init__(self, request):
        self.request = request

        if request.method == 'GET':
            self.input_data = request.GET.dict()
        else:
            self.input_data = request.data

    def post(self):
        if not self.input_data:
            return {'message': 'Error! data is missing.', 'data': {}, 'status': False}, BadRequest
        if 'first_name' not in self.input_data:
            return {'message': 'Error! First Name is missing.', 'data': {}, 'status': False}, BadRequest
        if 'email' not in self.input_data:
            return {'message': 'Error! email is missing.', 'data': {}, 'status': False}, BadRequest
        if 'phone_number' not in self.input_data:
            return {'message': 'Error! phone_number is missing.', 'data': {}, 'status': False}, BadRequest
        try:
            slz = SubmitCVSerializer(data=self.input_data)
            if slz.is_valid():
                slz.save()
            else:
                return {'message': 'Error! ' + str(slz.errors), 'data': {}, 'status': False}, BadRequest
        except Exception as e:
            return {'message': 'Error! ' + str(e), 'data': {}, 'status': False}, BadRequest
        return {'message': 'Success! Your CV is successfully submitted.', 'data': {}, 'status': True}, OK


class SearchJobHelper:
    def __init__(self, request):
        self.request = request

        if request.method == 'GET':
            self.input_data = request.GET.dict()
        else:
            self.input_data = request.data

    def post(self):
        if not self.input_data:
            return {'message': 'Error! data is missing.', 'data': {}, 'status': False}, BadRequest
        if 'page' not in self.input_data:
            return {'message': 'Error! page is required.', 'data': {}, 'status': False}, BadRequest
        if 'keyword' not in self.input_data or type(self.input_data['keyword']) is not list:
            return {'message': 'Error! keyword is required in array format.', 'data': {}, 'status': False}, BadRequest
        if 'location' not in self.input_data or type(self.input_data['location']) is not list:
            return {'message': 'Error! location is required in array format.', 'data': {}, 'status': False}, BadRequest
        try:
            limit = 20
            if 'limit' in self.input_data and self.input_data['limit'] and type(self.input_data['limit']) == int:
                limit = self.input_data['limit']
            if self.input_data['page'] < 0:
                return {'message': 'Error! page not allowed.', 'data': {},
                        'status': False}, BadRequest
            from_limit = self.input_data['page'] * limit
            to_limit = self.input_data['page'] * limit + limit

            query = Q()
            if self.input_data['keyword']:
                query |= Q(reduce(operator.or_, (Q(job_title__icontains=x.title()) for x in
                                                 self.input_data['keyword'])))
                # query |= Q(reduce(operator.or_, (Q(job_type__icontains=x.title()) for x in
                #                                  self.input_data['keyword'])))
                # query |= Q(
                #     reduce(operator.or_, (Q(experience_level__icontains=x.title()) for x in
                #                           self.input_data['keyword'])))
                query |= Q(reduce(operator.or_, (Q(roles_and_responsiblities__icontains=x.title()) for x in
                                                 self.input_data['keyword'])))
                # query |= Q(reduce(operator.or_,
                #                   (Q(experience_requirement__icontains=x.title()) for x in
                #                    self.input_data['keyword'])))
                query |= Q(reduce(operator.or_,
                                  (Q(skill_and_certification__icontains=x.title()) for x in
                                   self.input_data['keyword'])))

            if self.input_data['location']:
                query &= Q(reduce(operator.or_, (Q(job_location__icontains=x) for x in
                                                 self.input_data['location'])))

            if 'sector' in self.input_data and self.input_data['sector']:
                query &= Q(sector__icontains=self.input_data['sector'])

            if 'job_type' in self.input_data and self.input_data['job_type']:
                query &= Q(job_type__icontains=self.input_data['job_type'])
            if 'remote_job' in self.input_data:
                query &= Q(remote_job=self.input_data['remote_job'])
            data = list(
                SubmitJob.objects.distinct().filter(query)[from_limit: to_limit].values('id', 'first_name', 'last_name',
                                                                                        'email', 'remote_job', 
                                                                                        'company', 'job_title',
                                                                                        'phone_number',
                                                                                        'job_type',
                                                                                        'sector', 'job_location',
                                                                                        'experience_level',
                                                                                        'salary_budget',
                                                                                        'job_description',
                                                                                        'roles_and_responsiblities',
                                                                                        'experience_requirement',
                                                                                        'skill_and_certification',
                                                                                        'jd_link',
                                                                                        'created_on'))


        except Exception as e:
            print()
            data = []
        total_count = SubmitJob.objects.distinct().filter(query).count()
        page_length = math.ceil(SubmitJob.objects.distinct().filter(query).count() / limit)

        return {'message': '', 'data': data, 'total_count': total_count,
                'previous_page': self.input_data['page'] - 1 if self.input_data['page'] > 0 else self.input_data[
                    'page'],
                'next_page': self.input_data['page'] + 1, 'page_length': page_length, 'status': True}, OK


class SearchAllHelper:
    def __init__(self, request):
        self.request = request

        if request.method == 'GET':
            self.input_data = request.GET.dict()
        else:
            self.input_data = request.data

    def get(self):
        if not self.input_data:
            return {'message': 'Error! data is missing.', 'data': {}, 'status': False}, BadRequest
        if 'keyword' not in self.input_data:
            return {'message': 'Error! keyword is required in array format.', 'data': {}, 'status': False}, BadRequest

        try:
            remote_job = False
            if 'remote' in self.input_data['keyword']:
                remote_job = True
            jobs = list(SubmitJob.objects.filter(
                Q(job_type__icontains=self.input_data['keyword']) |
                Q(job_title__icontains=self.input_data['keyword']) |
                Q(skill_and_certification__icontains=self.input_data['keyword']) |
                Q(roles_and_responsiblities__icontains=self.input_data['keyword']) |
                Q(job_location__icontains=self.input_data['keyword']) |
                Q(sector__icontains=self.input_data['keyword'])
            ).distinct().values())
            blogs = list(Blog.objects.filter(
                Q(type__icontains=self.input_data['keyword']) |
                Q(heading__icontains=self.input_data['keyword']) |
                Q(small_description__icontains=self.input_data['keyword'])
            ).distinct().values())
            courses = list(Course.objects.filter(
                Q(name__icontains=self.input_data['keyword']) |
                Q(category__icontains=self.input_data['keyword']) |
                Q(brief_description__icontains=self.input_data['keyword'])
            ).distinct().values())
            training = list(Training.objects.filter(
                Q(name__icontains=self.input_data['keyword']) |
                Q(category__icontains=self.input_data['keyword']) |
                Q(brief_description__icontains=self.input_data['keyword'])
            ).distinct().values())

            data = {
                'jobs': jobs,
                'blogs': blogs,
                'courses': courses,
                'training': training
            }

        except Exception as e:
            print(e)
            data = {}

        return {'message': '', 'data': data, 'status': True}, OK


class FieldHelper:
    def __init__(self, request):
        self.request = request
        self.input_data = request.GET

    def get(self):
        if not self.input_data:
            return {'message': 'Error! data is missing.', 'data': {}, 'status': False}, BadRequest
        if 'field' not in self.input_data or not self.input_data['field']:
            return {'message': 'Error! field is required in array format.', 'data': {}, 'status': False}, BadRequest
        if self.input_data['field'] == 'location':
            data = set(SubmitJob.objects.all().values_list('job_location', flat=True))
        elif self.input_data['field'] == 'skill':
            data = set(SubmitJob.objects.all().values_list('skill_and_certification', flat=True))
        elif self.input_data['field'] == 'company':
            data = set(SubmitJob.objects.all().values_list('company', flat=True))
        elif self.input_data['field'] == 'job_title':
            data = set(SubmitJob.objects.all().values_list('job_title', flat=True))
        elif self.input_data['field'] == 'training_type':
            from training.models import Type
            data = list(Type.objects.all().values('id', 'name'))
        elif self.input_data['field'] == 'training_topic':
            from training.models import Topic
            data = list(Topic.objects.all().values('id', 'name'))
        elif self.input_data['field'] == 'course_type':
            from cources.models import Type
            data = list(Type.objects.all().values('id', 'name'))
        elif self.input_data['field'] == 'course_topic':
            from cources.models import Topic
            data = list(Topic.objects.all().values('id', 'name'))
        elif self.input_data['field'] == 'certification':
            from cources.models import Course
            data = list(Course.objects.all().values('id', 'name'))
        else:
            return {'message': 'Error! invalid field.', 'data': {}, 'status': False}, BadRequest
        return {'message': '', 'data': data, 'status': True}, OK
