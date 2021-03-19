import os
import os.path
import pickle
import string
from datetime import datetime
from uuid import uuid4

import boto3
from django.core.files.storage import default_storage, FileSystemStorage
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
S3_BUCKET = os.environ.get("S3_BUCKET")

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


class UploadService(APIView):
    def post(self, request):
        file = request.FILES['file']
        name = file.name
        extension = name.split(".")[-1]
        random = id_generator(4) + '-' + id_generator(8)
        path = random + "." + extension
        try:
            # uploaded = file.save(path)
            uploaded = upload(file, path)
        except Exception as e:
            print(e)
            return JsonResponse({'status': False, 'message': 'error', 'data': {}}, status=400)

        return JsonResponse({'status': True,
                             'message': "file uploaded",
                             'data': uploaded}, status=200)


def id_generator(size=8,
                 chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return uuid4().hex + str(datetime.now().time().microsecond)


def upload(file, path, acl="public-read"):
    try:
        print(path, S3_BUCKET)
        res = s3.upload_fileobj(
            file,
            S3_BUCKET,
            os.environ.get('CDN_PATH') + path,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
        # print("PATH: ",s3_path)

    except Exception as e:
        print("Something Happened: ", e)
        return JsonResponse({'uploaded': False,
                             'error': "s3 error"
                             })
    path = f"{os.environ.get('S3_PATH')}{os.environ.get('CDN_PATH')}{path}"
    return path
