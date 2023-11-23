from django.shortcuts import get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import permission_required
# from django.core.exceptions import PermissionDenied
from rest_framework import status, permissions, viewsets
# from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
# from djoser.views import UserViewSet

from .models import CustomBaseUser
from .serializers import (UserSerializer, UserSubscribeSerializer,
                          UserForAnonSerializer)
from .permissions import OwnProfilePermission


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomBaseUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'list',)
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return UserSerializer
        return UserForAnonSerializer

    @action(
        methods=['get', 'patch'], detail=False,
        url_path='me', permission_classes=(OwnProfilePermission,),
    )
    def me(self, request):
        if request.method == 'GET':
            user = get_object_or_404(CustomBaseUser, email=request.user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        user = get_object_or_404(CustomBaseUser, email=request.user)
        serializer = self.serializer_class(user, data=request.data,
                                           partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# class SubscribtionViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     http_method_names = ('get', 'post', 'delete')

#     def get_queryset(self):
#         queryset = self.request.user.subscribe.objects.all()
#         return queryset


@api_view(['POST', 'DELETE'])
def subscribe(request, pk):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    subscribed_user = get_object_or_404(CustomBaseUser, id=pk)
    check = request.user.subscribe.filter(
        email=subscribed_user.email
    ).exists()
    if request.method == 'POST':
        if not check and request.user != subscribed_user:
            request.user.subscribe.add(subscribed_user)
            serializer = UserSubscribeSerializer(subscribed_user,
                                                 context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        if check:
            request.user.subscribe.remove(subscribed_user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
