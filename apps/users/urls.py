from django.conf.urls import url
from .views import UserInfoView,UserFavView,UserCommentView,ChangePwdView,UpLoadImageView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^fav/$', UserFavView.as_view(), name='user_fav'),
    url(r'^comment/$', UserCommentView.as_view(), name='user_comment'),
    url(r'^change/$', ChangePwdView.as_view(), name='change_pwd'),
    url(r'^up_photo/$', UpLoadImageView.as_view(), name='up_photo'),
]
