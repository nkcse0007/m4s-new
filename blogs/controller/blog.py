import json
from common.json_response import *
from blogs.models import Blog, Comment, Like, CommentReply
from common.com import *
from blogs.serializers import BlogSerializer, CommentSerializer, CommentReplySerializer, LikeSerializer
import math
import os

class BlogHelper:
    def __init__(self, request):
        self.request = request

        if request.method == 'GET':
            self.input_data = request.GET.dict()
        else:
            self.input_data = request.data

    def post(self):
        if 'page' not in self.input_data:
            return {'message': 'Error! page is required.', 'data': {}, 'status': False}, BadRequest
        if 'type' not in self.input_data or not self.input_data:
            return {'message': 'Error! type is missing.', 'data': {}, 'status': False}, BadRequest
        if 'id' in self.input_data:
          
            blogs = Blog.objects.filter(id=self.input_data['id']).values().last()
            data['image'] = os.environ.get('S3_FILE_PATH')+data['image']
            data['icon'] = os.environ.get('S3_FILE_PATH')+data['icon']
            blogs['comments'] = list(Comment.objects.filter(blog=self.input_data['id']).values())
            blogs['likes'] = Like.objects.filter(blog=self.input_data['id'], type='LIKE').count()
            return {'message': '', 'data': blogs, 'status': True}, OK

        else:
            limit = 20
            if 'limit' in self.input_data and self.input_data['limit'] and type(self.input_data['limit']) == int:
                limit = self.input_data['limit']
            if self.input_data['page'] < 0:
                return {'message': 'Error! page not allowed.', 'data': {},
                        'status': False}, BadRequest
            from_limit = self.input_data['page'] * limit
            to_limit = self.input_data['page'] * limit + limit

            blogs = list(
                Blog.objects.filter(type=self.input_data['type'])[from_limit: to_limit].values('id', 'heading', 'image', 'icon',
                                                                                               'category', 'date',
                                                                                               'author', 'created_on'))

            for blog in blogs:
                blog['image'] = [os.environ.get('S3_FILE_PATH')+blog['image']]
                blog['icon'] = [os.environ.get('S3_FILE_PATH')+blog['icon']]
                blog['comments'] = Comment.objects.filter(blog=blog['id']).count()
                blog['likes'] = Like.objects.filter(blog=blog['id'], type='LIKE').count()
            total_count = Blog.objects.filter(type=self.input_data['type']).count()
            page_length = math.ceil(Blog.objects.filter(type=self.input_data['type']).count() / limit)
            return {'message': '', 'data': blogs, 'total_count': total_count,
                    'previous_page': self.input_data['page'] - 1 if self.input_data['page'] > 0 else self.input_data[
                        'page'],
                    'next_page': self.input_data['page'] + 1, 'page_length': page_length, 'status': True}, OK


class CommentHelper:
    def __init__(self, request):
        self.request = request
        self.input_data = request.data

    def get(self):
        if 'blog' not in self.input_data or not self.input_data['blog']:
            return {'message': 'Error! blog id is required.', 'data': {}, 'status': False}, BadRequest

        comments = list(Comment.objects.filter(blog=self.input_data['blog_id']).values())
        return {'message': '', 'data': comments, 'status': True}, OK

    def post(self):
        if 'blog' not in self.input_data or not self.input_data['blog']:
            return {'message': 'Error! blog id is required.', 'data': {}, 'status': False}, BadRequest
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
        if 'blog_id' not in self.input_data or not self.input_data['blog_id']:
            return {'message': 'Error! blog_id is required.', 'data': {}, 'status': False}, BadRequest
        if 'type' not in self.input_data or not self.input_data['type']:
            return {'message': 'Error! type is required.', 'data': {}, 'status': False}, BadRequest

        likes = Like.objects.filter(blog=self.input_data['blog_id'], type=self.input_data['type']).count()
        return {'message': '', 'data': likes, 'status': True}, OK

    def post(self):
        if 'blog' not in self.input_data or not self.input_data['blog']:
            return {'message': 'Error! blog id is required.', 'data': {}, 'status': False}, BadRequest
        if 'type' not in self.input_data or not self.input_data['type']:
            return {'message': 'Error! type is required.', 'data': {}, 'status': False}, BadRequest

        slz = LikeSerializer(data=self.input_data)
        if slz.is_valid():
            slz.save()
        else:
            return {'message': 'Error! ' + str(slz.errors), 'data': {}, 'status': False}, BadRequest

        return {'message': 'Success! Comment created.', 'data': {}, 'status': True}, OK
