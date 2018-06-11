from .models import VideoComments,UserFavorite,UserMessage,CommentsPraise
import xadmin

class VideoCommentsAdmin(object):
    list_display = ['user', 'video', 'comments', 'add_time']
    search_fields = ['user', 'video', 'comments']
    list_filter = ['user', 'video', 'comments', 'add_time']
class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id','add_time']
    search_fields = ['user', 'fav_id']
    list_filter = ['user', 'fav_id','add_time']
class UserMessageAdmin(object):
        list_display = ['user', 'Message', 'has_read', 'add_time']
        search_fields = ['user', 'Message', 'has_read']
        list_filter =['user', 'Message', 'has_read', 'add_time']
class CommentsPraiseAdmin(object):
    list_display = ['user', 'comment']
    search_fields = ['user', 'comment']
    list_filter = ['user', 'comment']

xadmin.site.register(VideoComments,VideoCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(CommentsPraise,CommentsPraiseAdmin)
