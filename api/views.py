from rest_framework import viewsets, generics, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import NewsPost, Category, Tags, UserNewsPostRelation, UserSubscription
from .serializers import NewsPostSerializer, UserSerializer, LoginSerializer, CategorySerializer, TagsSerializer, UserNewsPostRelationSerializer, UserSubscriptionSerializer, UserRegisterSerializer
from .permissions import PermissionByAction

## Registration View is not necessary ##
class RegisterUserView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_serializer = UserRegisterSerializer(user, many=False, context={'request': request})
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["token"] = {"refresh": str(token), "access": str(token.access_token)}
        data.update(user_serializer)
        return Response(data, status=status.HTTP_201_CREATED)


class LoginUserApi(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            user_serializer = UserSerializer(user)
            token = RefreshToken.for_user(user)
            data = user_serializer.data
            data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
            data.update(user_serializer)
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'Incorrect password or username'}, status=status.HTTP_401_UNAUTHORIZED)


class NewsPostView(viewsets.ModelViewSet):
    queryset = NewsPost.objects.all()
    serializer_class = NewsPostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly()]
    allowed_actions = {
        'admin': ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy'],
        'author': ['list', 'create', 'retrieve', 'update', 'partial_update'],
        'user': ['list', 'retrieve']
    }

    def get_permissions(self):
        if self.request.user.is_authenticated:
            role = self.request.user.role

            allowed_actions = self.allowed_actions.get(role, [])

            permission_classes = [PermissionByAction(allowed_actions)]

            return [permission() for permission in permission_classes]

        return self.permission_classes


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, ]
    permission_classes = [IsAuthenticatedOrReadOnly()]
    allowed_actions = {
        'admin': ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy'],
        'author': ['list', 'create', 'retrieve', 'update', 'partial_update'],
        'user': ['list', 'retrieve']
    }

    def get_permissions(self):
        if self.request.user.is_authenticated:
            role = self.request.user.role

            allowed_actions = self.allowed_actions.get(role, [])

            permission_classes = [PermissionByAction(allowed_actions)]

            return [permission() for permission in permission_classes]
        return self.permission_classes


class TagsView(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    filter_backends = [DjangoFilterBackend, ]
    permission_classes = [IsAuthenticatedOrReadOnly,]
    allowed_actions = {
        'admin': ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy'],
        'author': ['list', 'create', 'retrieve', 'update', 'partial_update'],
        'user': ['list', 'retrieve']
    }

    def get_permissions(self):
        if self.request.user.is_authenticated:
            role = self.request.user.role

            allowed_actions = self.allowed_actions.get(role, [])

            permission_classes = [PermissionByAction(allowed_actions)]

            return [permission() for permission in permission_classes]
        return self.permission_classes


class UserNewsPostRelationView(viewsets.ModelViewSet):
    queryset = UserNewsPostRelation.objects.all()
    serializer_class = UserNewsPostRelationSerializer
    permission_classes = [IsAuthenticated, ]


class UserSubscriptionView(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated, ]
