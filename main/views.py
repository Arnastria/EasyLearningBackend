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

from django.http.response import HttpResponseRedirect
# Create your views here.


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def sample_api(request):
    """
    Just an overly simple sample enpoint to call.
    """
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = 'API Call succeed on %s' % time
    return Response({'message': message})


# TODO: Refactor login, logout, token to viewset

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
@with_sso_ui()
def login(request, sso_profile):
    """
    Handle SSO UI login.
    Create a new user & profile if it doesn't exists
    and return token if SSO login suceed.
    """
    origin = request.GET.get('origin', '')
    if sso_profile is not None:
        token = process_sso_profile(sso_profile)
        username = sso_profile['username']
        if origin is not None:
            return redirect('%s/loginSuccess/%s' % ('https://www.easy-learning.my.id', token))
        return HttpResponseRedirect(
            '/token?token=%s&username=%s' % (token, username))

    data = {'message': 'invalid sso'}
    if origin is not None:
        return redirect('%s/loginError' % (origin))

    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
@with_sso_ui()
def login_backup(request, sso_profile):
    """
    Handle SSO UI login.
    Create a new user & profile if it doesn't exists
    and return token if SSO login suceed.
    """
    origin = request.GET.get('origin', '')
    if sso_profile is not None:
        token = process_sso_profile(sso_profile)
        username = sso_profile['username']
        if origin is not None:
            return redirect('%s/loginSuccess/%s' % ('https://easy-learning-platform.herokuapp.com', token))
        return HttpResponseRedirect(
            '/token?token=%s&username=%s' % (token, username))

    data = {'message': 'invalid sso'}
    if origin is not None:
        return redirect('%s/loginError' % (origin))

    return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def token(request):
    return Response(request.GET)


@api_view(['GET'])
def logout(request):
    """
    Handle SSO UI logout.
    Remember that this endpoint require Token Authorization. 
    """
    return HttpResponseRedirect(get_logout_url(request))


@api_view(['GET'])
# Default permission for any endpoint: permissions.IsAuthenticated
def restricted_sample_endpoint(request):
    """
    Simple sample enpoint that require Token Authorization.
    """
    message = 'If you can see this, it means you\'re already logged in.'
    username = request.user.username
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
    else:
        profile = None
    # It's just quick hacks for temporary output.
    # Should be used Django Rest Serializer instead.
    profile_json = serializers.serialize('json', [profile])
    return Response({'message': message})


@api_view(['GET'])
def get_profile(request):
    username = request.user.username
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
    else:
        profile = None
    profile_json = serializers.serialize('json', [profile])
    return Response({'username': username,
                     'profile': profile_json})


@api_view(['POST'])
def test_post(request):
    if(request.body != None):
        json_data = json.loads(request.body)
        print(json_data)
    return Response({
        'body': request.body
    })
