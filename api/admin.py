from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import NewsPost, Category, Tags, UserNewsPostRelation, UserSubscription


class NewsPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = NewsPost
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsPostAdminForm


admin.site.register(NewsPost, NewsAdmin)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(UserNewsPostRelation)
admin.site.register(UserSubscription)


