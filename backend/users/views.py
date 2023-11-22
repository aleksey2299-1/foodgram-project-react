from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer, SelfUserSerializer
from .permissions import OwnProfilePermission

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        methods=['get', 'patch'], detail=False,
        url_path='me', permission_classes=(OwnProfilePermission,),
    )
    def me_user(self, request):
        if request.method == 'GET':
            user = get_object_or_404(
                User, username=request.user,
            )
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        user = get_object_or_404(
            User, username=request.user,
        )
        serializer = SelfUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
