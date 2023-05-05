from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin, BaseUserManager
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

#User = get_user_model()


class User(AbstractUser):
    ADMIN = 'admin'
    AUTHOR = 'author'
    USER = 'user'
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (AUTHOR, 'Author'),
        (USER, 'User'),
    )
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phone = models.CharField(_('Phone number'), max_length=20, null=True)
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default=USER, verbose_name=_('choice role'))


#class CustomUserManager(BaseUserManager):
#    def create_user(self, email, password, **extra_fields):
#        if not email:
#            raise ValueError(_('The Email field must be set'))
#        email = self.normalize_email(email)
#        user = self.model(email=email, **extra_fields)
#        user.set_password(password)
#        user.save()
#        return user

#    def create_superuser(self, email, password, **extra_fields):
#        extra_fields.setdefault('is_staff', True)
#        extra_fields.setdefault('is_superuser', True)
#        extra_fields.setdefault('is_active', True)

#        if extra_fields.get('is_superuser') is not True:
#            raise ValueError('Superuser must be True')
#        return self.create_user(email, password, **extra_fields)


#class User(AbstractBaseUser, PermissionsMixin):
#    email = models.EmailField(_('email address'), unique=True)
#    first_name = models.CharField(_('first name'), max_length=30, blank=True)
#    last_name = models.CharField(_('last name'), max_length=30, blank=True)
#    phone = models.CharField(_('Phone number'), max_length=20, null=True)
#    is_active = models.BooleanField(_('user'), default=False)
#    is_staff = models.BooleanField(_('admin'), default=False)
#    is_superuser = models.BooleanField(_('author'), default=True)
#    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

#    objects = CustomUserManager()

#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = ['first_name', 'last_name']

#    class Meta:
#        verbose_name = _('user')
#        verbose_name_plural = _('users')

#    def __str__(self):
#        return self.email


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name=_('category title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=150, verbose_name=_('tag title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def __str__(self):
        return self.title


class NewsPost(models.Model):
    title = models.CharField(max_length=150, verbose_name=_('news title'))
    slug = models.SlugField(max_length=100, unique=True, null=True)
    description = models.CharField(max_length=255, verbose_name=_('description'))
    content = RichTextField(verbose_name=_('content'))
    data = models.TextField(verbose_name=_('information'))
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('category'), default='sport')
    tags = models.ManyToManyField(Tags, verbose_name=_('tags'), default='any tags')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_news_post', verbose_name=_('author'))
    readers = models.ManyToManyField(User, through='UserNewsPostRelation', related_name='news_post', verbose_name=_('readers'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def __str__(self):
        return self.title


class UserNewsPostRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    newsPost = models.ForeignKey(NewsPost, on_delete=models.CASCADE, verbose_name=_('news'))
    like = models.BooleanField(default=False)
    save = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} {self.newsPost}"


class UserSubscription(models.Model):
    user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
