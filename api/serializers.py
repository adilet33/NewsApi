from rest_framework import serializers
from django.contrib.auth import authenticate
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.password_validation import validate_password
from .models import NewsPost, Category, User, Tags, UserNewsPostRelation, UserSubscription
from .admin import NewsPostAdminForm


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'username',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'username', 'role', 'password']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class NewsPostSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    category = CategorySerializer(read_only=True)
    tags = TagsSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    readers = UserSerializer(read_only=True)

    class Meta:
        model = NewsPost
        fields = '__all__'

    def create(self, validated_data):
        form = NewsPostAdminForm(validated_data)
        instance = form.save()
        return instance


class UserNewsPostRelationSerializer(serializers.ModelSerializer):
    newsPost = NewsPostSerializer(read_only=True)

    class Meta:
        model = UserNewsPostRelation
        fields = ('newsPost', 'like', 'save')


class UserSubscriptionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = UserSubscription
        fields = ('author', )
