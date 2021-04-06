import json
import operator
from functools import reduce
import os
from common.com import *
from common.json_response import *
from dateutil.parser import parse
from django.db.models import Q
from cources.models import Course, Comment, CommentReply, Like
import math


class CourseHelper:
    def __init__(self, request):
        self.request = request
        if request.method == 'GET':
            self.input_data = request.GET.dict()
        else:
            self.input_data = request.data

    def post(self):
        if 'id' in self.input_data:
            data = Course.objects.filter(id=self.input_data['id']).values().last()
            data['image'] = os.environ.get('S3_FILE_PATH')+data['image']
            data['icon'] = os.environ.get('S3_FILE_PATH')+data['icon']
            data['comments'] = list(Comment.objects.filter(course=self.input_data['id']).values())
            data['likes'] = Like.objects.filter(course=self.input_data['id'], type='LIKE').count()
            return {'message': '', 'data': data, 'status': True}, OK
        else:
            if 'page' not in self.input_data:
                return {'message': 'Error! page is required.', 'data': {}, 'status': False}, BadRequest

            limit = 20
            if 'limit' in self.input_data and self.input_data['limit'] and type(self.input_data['limit']) == int:
                limit = self.input_data['limit']
            if self.input_data['page'] < 0:
                return {'message': 'Error! page not allowed.', 'data': {},
                        'status': False}, BadRequest
            from_limit = self.input_data['page'] * limit
            to_limit = self.input_data['page'] * limit + limit

            query = Q()

            if 'topic' in self.input_data and type(self.input_data['topic']) is list and self.input_data['topic']:
                query &= Q(topic__in=self.input_data['topic'])
            if 'type' in self.input_data and type(self.input_data['type']) is list and self.input_data['type']:
                query &= Q(type__in=self.input_data['type'])
            if 'category' in self.input_data and type(self.input_data['category']) is list and self.input_data['category']:
                query &= Q(category__in=self.input_data['category'])
            if 'is_online' in self.input_data:
                query &= Q(is_online=self.input_data['is_online'])
            if 'in_person' in self.input_data:
                query &= Q(in_person=self.input_data['in_person'])
            if 'keyword' in self.input_data and self.input_data['keyword']:
                query &= Q(name__icontains=self.input_data['keyword'])
            data = list(Course.objects.distinct().filter(query)[from_limit: to_limit].values())
            for blog in data:
                blog['image'] = [os.environ.get('S3_FILE_PATH')+blog['image']]
                blog['icon'] = [os.environ.get('S3_FILE_PATH')+blog['icon']]
                blog['comments'] = Comment.objects.filter(course=blog['id']).count()
                blog['likes'] = Like.objects.filter(course=blog['id'], type='LIKE').count()

            total_count = Course.objects.filter(query).count()
            page_length = math.ceil(Course.objects.filter(query).count() / limit)

            return {'message': '', 'data': data, 'total_count': total_count,
                    'previous_page': self.input_data['page'] - 1 if self.input_data['page'] > 0 else self.input_data[
                        'page'],
                    'next_page': self.input_data['page'] + 1, 'page_length': page_length, 'status': True}, OK



class CommentHelper:
    def __init__(self, request):
        self.request = request
        self.input_data = request.data

    def get(self):
        if 'course' not in self.input_data or not self.input_data['course']:
            return {'message': 'Error! course id is required.', 'data': {}, 'status': False}, BadRequest

        comments = list(Comment.objects.filter(course=self.input_data['course']).values())
        return {'message': '', 'data': comments, 'status': True}, OK

    def post(self):
        if 'course' not in self.input_data or not self.input_data['course']:
            return {'message': 'Error! course id is required.', 'data': {}, 'status': False}, BadRequest
        if 'comment' not in self.input_data or not self.input_data['comment']:
            return {'message': 'Error! comment is required.', 'data': {}, 'status': False}, BadRequest

        slz = CommentSerializer(data=self.input_data)
        if slz.is_valid():
            slz.save()
        else:
            return {'message': 'Error! ' + str(slz.errors), 'data': {}, 'status': False}, BadRequest

        return {'message': 'Success! Comment created.', 'data': {}, 'status': True}, OK


class CommentReplyHelper:
    def __init__(self, request):
        self.request = request
        self.input_data = request.data

    def get(self):
        if 'comment' not in self.input_data or not self.input_data['comment']:
            return {'message': 'Error! comment id is required.', 'data': {}, 'status': False}, BadRequest

        comments_replies = list(CommentReply.objects.filter(comment=self.input_data['comment']).values())
        return {'message': '', 'data': comments_replies, 'status': True}, OK

    def post(self):

        if 'comment' not in self.input_data or not self.input_data['comment']:
            return {'message': 'Error! comment id is required.', 'data': {}, 'status': False}, BadRequest
        if 'reply' not in self.input_data or not self.input_data['reply']:
            return {'message': 'Error! reply is required.', 'data': {}, 'status': False}, BadRequest

        slz = CommentReplySerializer(data=self.input_data)
        if slz.is_valid():
            slz.save()
        else:
            return {'message': 'Error! ' + str(slz.errors), 'data': {}, 'status': False}, BadRequest

        return {'message': 'Success! Reply created.', 'data': {}, 'status': True}, OK


class LikeHelper:
    def __init__(self, request):
        self.request = request
        self.input_data = request.data

    def get(self):
        if 'course' not in self.input_data or not self.input_data['course']:
            return {'message': 'Error! course is required.', 'data': {}, 'status': False}, BadRequest
        if 'type' not in self.input_data or not self.input_data['type']:
            return {'message': 'Error! type is required.', 'data': {}, 'status': False}, BadRequest

        likes = Like.objects.filter(course=self.input_data['course'], type=self.input_data['type']).count()
        return {'message': '', 'data': likes, 'status': True}, OK

    def post(self):
        if 'course' not in self.input_data or not self.input_data['course']:
            return {'message': 'Error! course id is required.', 'data': {}, 'status': False}, BadRequest
        if 'type' not in self.input_data or not self.input_data['type']:
            return {'message': 'Error! type is required.', 'data': {}, 'status': False}, BadRequest

        slz = LikeSerializer(data=self.input_data)
        if slz.is_valid():
            slz.save()
        else:
            return {'message': 'Error! ' + str(slz.errors), 'data': {}, 'status': False}, BadRequest

        return {'message': 'Success! Comment created.', 'data': {}, 'status': True}, OK

