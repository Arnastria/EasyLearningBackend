# from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from datetime import datetime
from .utils import process_sso_profile
from sso.decorators import with_sso_ui
from sso.utils import get_logout_url
from django.core import serializers
from django_auto_prefetching import AutoPrefetchViewSetMixin
from django.shortcuts import redirect
import json
from .models import *

from django.http.response import HttpResponseRedirect, HttpResponseServerError
# Create your views here.


@api_view(['POST'])
def api_test_post(request):
    if(request.body != None):
        json_data = json.loads(request.body)
        print(json_data)
    return Response({
        'body': request.body
    })

# API SET FOR COURSE
#
#
#


@api_view(['POST'])
def create_course(request):
    try:
        if(request.body != None):
            json_data = json.loads(request.body)
            model = Course.objects.create(
                code=json_data['code'],
                name=json_data['name'],
                aliasName=json_data['aliasName'],
                intro=json_data['intro'],
                description=json_data['description'],
                links=json_data['links'],
            )
            model.save()
            model_json = serializers.serialize('json', [model])
            return Response({'model': model_json})
        else:
            return HttpResponseServerError("No Body Data!")

    except Exception as e:
        return HttpResponseServerError(str(e))


@api_view(['GET'])
def get_all_course(request):
    try:
        model = Course.objects.all()
        model_json = serializers.serialize('json', model)
        return Response({
            'model': model_json})
    except:
        return HttpResponseServerError("No data found")


@api_view(['GET'])
def get_course(request, id):
    try:
        model = Course.objects.get(pk=id)
        model_json = serializers.serialize('json', [model])
        return Response({
            'model': model_json})
    except:
        return HttpResponseServerError("No data found")


# API SET FOR MATERIAL
#
#
#
@api_view(['POST'])
def create_material(request, id_course):
    try:
        course = Course.objects.get(pk=id_course)
        if(request.body != None):
            json_data = json.loads(request.body)
            model = Material.objects.create(
                course=course,
                name=json_data['name'],
                intro=json_data['intro'],
                description=json_data['description'],
                pdf=json_data['pdf'],
                pdf_chapter=json_data['pdf_chapter'],
                links=json_data['links'],
            )
            model.save()
            model_json = serializers.serialize('json', [model])
            return Response({'model': model_json})
        else:
            return HttpResponseServerError("No Body Data!")

    except Exception as e:
        return HttpResponseServerError(str(e))


@api_view(['GET'])
def get_all_material(request):
    try:
        model = Material.objects.all()
        model_json = serializers.serialize('json', model)
        return Response({
            'model': model_json})
    except:
        return HttpResponseServerError("No data found")


@api_view(['GET'])
def get_material(request, id):
    try:
        model = Material.objects.get(pk=id)
        model_json = serializers.serialize('json', [model])
        return Response({
            'model': model_json})
    except:
        return HttpResponseServerError("No data found")


@api_view(['GET'])
def get_material_by_course(request, id_course):
    try:
        course = Course.objects.get(pk=id_course)
        materials = Material.objects.filter(course=course)
        model_json = serializers.serialize('json', materials)
        return Response({
            'materials': model_json})
    except:
        return HttpResponseServerError("No data found")


# API SET FOR POST
#
#
#
@api_view(['POST'])
def create_post(request, id_material):
    try:
        material = Material.objects.get(pk=id_material)
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
        else:
            return HttpResponseServerError("No Profile Found!")
        if(request.body != None):
            json_data = json.loads(request.body)
            model = Post.objects.create(
                material=material,
                profile=profile,
                author_name=profile.name,
                body=json_data['body'],
                title=json_data['title'],
                category=json_data['category'],
                date=datetime.utcnow()
            )
            model.save()
            model_json = serializers.serialize('json', [model])
            return Response({'model': model_json})
        else:
            return HttpResponseServerError("No Body Data!")

    except Exception as e:
        return HttpResponseServerError(str(e))


@api_view(['GET'])
def get_post(request, id):
    try:
        model = Post.objects.get(pk=id)
        model_json = serializers.serialize('json', [model])
        return Response({
            'model': model_json})
    except:
        return HttpResponseServerError("No data found")


@api_view(['POST'])
def update_post(request, id):
    try:
        model = Post.objects.get(pk=id)
        if(request.body != None):
            json_data = json.loads(request.body)
            model.body = json_data['body']
            model.title = json_data['title']
            model.save()
            model_json = serializers.serialize('json', [model])
            return Response({'model': model_json})
        else:
            return HttpResponseServerError("No Body Data!")
    except:
        return HttpResponseServerError("No data found")


@api_view(['GET'])
def get_post_by_material(request, id_material):
    try:
        material = Material.objects.get(pk=id_material)
        posts = Post.objects.filter(material=material)
        model_json = serializers.serialize('json', posts)
        return Response({
            'post': model_json})
    except:
        return HttpResponseServerError("No data found")


@api_view(['GET'])
def get_latest_post_by_material(request, id_material):
    try:
        material = Material.objects.get(pk=id_material)
        posts = Post.objects.filter(material=material).order_by('-id')[0]
        model_json = serializers.serialize('json', [posts])
        return Response({
            'post': model_json})
    except:
        return HttpResponseServerError("No data found")


@api_view(['POST'])
def delete_post_by_id(request, id):
    try:
        post = Post.objects.filter(id=id)
        post.delete()
        return Response({'message': 'success delete'})
    except:
        return HttpResponseServerError("No data found")

# API SET FOR REPLY
#
#
#


@api_view(['POST'])
def create_reply(request, id_post):
    try:
        post = Post.objects.get(pk=id_post)
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
        else:
            return HttpResponseServerError("No Profile Found!")
        if(request.body != None):
            json_data = json.loads(request.body)
            model = Reply.objects.create(
                post=post,
                profile=profile,
                author_name=profile.name,
                body=json_data['body'],
                date=datetime.utcnow()
            )
            model.save()
            model_json = serializers.serialize('json', [model])
            return Response({'model': model_json})
        else:
            return HttpResponseServerError("No Body Data!")

    except Exception as e:
        return HttpResponseServerError(str(e))


@api_view(['GET'])
def get_reply(request, id):
    try:
        model = Reply.objects.get(pk=id)
        model_json = serializers.serialize('json', [model])
        return Response({
            'model': model_json})
    except:
        return HttpResponseServerError("No data found")


@api_view(['POST'])
def update_reply(request, id):
    try:
        model = Reply.objects.get(pk=id)
        if(request.body != None):
            json_data = json.loads(request.body)
            model.body = json_data['body']
            model.save()
            model_json = serializers.serialize('json', [model])
            return Response({'model': model_json})
        else:
            return HttpResponseServerError("No Body Data!")
    except:
        return HttpResponseServerError("No data found")


@api_view(['GET'])
def get_reply_by_post(request, id_post):
    try:
        post = Post.objects.get(pk=id_post)
        replies = Reply.objects.filter(post=post)
        model_json = serializers.serialize('json', replies)
        return Response({
            'replies': model_json})
    except:
        return HttpResponseServerError("No data found")


@api_view(['POST'])
def delete_reply_by_id(request, id):
    try:
        reply = Reply.objects.filter(id=id)
        reply.delete()
        return Response({'message': 'success delete'})
    except:
        return HttpResponseServerError("No data found")


@api_view(['GET'])
def get_pdf(request, id_pdf):
    try:
        model = PDFModel.objects.get(pk=id_pdf)
        model_json = serializers.serialize('json', [model])
        return Response({
            'model': model_json})
    except Exception as e:
        return HttpResponseServerError(str(e))
