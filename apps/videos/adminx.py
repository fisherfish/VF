from .models import Video, Season, Episode
import xadmin


class VideoAdmin(object):
    list_display = ['name','desc','detail','tags','video_times','click_nums']
    search_fields =['name','desc','detail','tags','click_nums']
    list_filter =['name','desc','detail','tags','video_times','click_nums']


class SeasonAdmin(object):
    list_display = ['name', 'video', 'add_time']
    search_fields = ['name', 'video']
    list_filter = ['name', 'video', 'add_time']


class EpisodeAdmin(object):
    list_display = ['name', 'season','url', 'add_time']
    search_fields = ['name', 'season','url']
    list_filter = ['name', 'season','url', 'add_time']

xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(Season,SeasonAdmin)
xadmin.site.register(Episode,EpisodeAdmin)