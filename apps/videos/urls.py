from django.conf.urls import url
from .views import MovieView,TView,DocView,AnimeView,VarietyView,VideoDetailView,PlayView,VideoNewView,VideoScoreView
from operation.views import AddFavView,AddCommentView,CommentPraiseView

urlpatterns = [
    url(r'^new/$', VideoNewView.as_view(), name='video_new'),
    url(r'^hot/$', VideoScoreView.as_view(), name='video_score'),
    url(r'^movie/$', MovieView.as_view(), name='movie'),
    url(r'^tv/$', TView.as_view(), name='tv'),
    url(r'^documentary/$', DocView.as_view(), name='documentary'),
    url(r'^anime/$', AnimeView.as_view(), name='anime'),
    url(r'^variety/$', VarietyView.as_view(), name='variety'),
    url(r'^detail/(?P<video_id>\d+)/$', VideoDetailView.as_view(), name='video_detail'),
    url(r'^play/(?P<video_id>\d+)/$', PlayView.as_view(), name='play'),
    url(r'^addcomment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^addfav/$', AddFavView.as_view(), name='add_fav'),
    url(r'^comment_praise/$',  CommentPraiseView.as_view(), name='comment_praise'),
]


