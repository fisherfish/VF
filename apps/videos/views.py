import datetime
import json

from django.shortcuts import render
from django.views.generic.base import View
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from .models import Video
from operation.models import VideoComments,UserFavorite

# 最新
class VideoNewView(View):
    def get(self,request):
        video = Video.objects.all().order_by('-add_time')
        page = request.GET.get('page', 1)
        p = Paginator(video, 18)
        video = p.page(int(page))
        last = p.num_pages
        return render(request, 'all-video.html',{
            'video':video,
            'plist':p.page_range,
            'last':last
        })
# 评分
class VideoScoreView(View):
    def get(self,request):
        video = Video.objects.all().order_by('-click_nums')
        page = request.GET.get('page', 1)
        p = Paginator(video, 18)
        video = p.page(int(page))
        last = p.num_pages
        return render(request, 'all-video.html',{
            'video':video,
            'plist':p.page_range,
            'last':last
        })
# 电影
class MovieView(View):
    def get(self, request):
       video = Video.objects.filter(tags='电影').order_by('-add_time')
       sort = request.GET.get('sort','')
       if sort == 'score':
           video = Video.objects.filter(tags='电影').order_by('-click_nums')
       page = request.GET.get('page', 1)
       p = Paginator(video, 18)
       video = p.page(int(page))
       plist = p.page_range
       tag = 'movie'
       return render(request,'movie-list.html',{
           'video':video,
           'plist':plist,
           'sort':sort,
           'tag':tag
       })
# 剧集
class TView(View):
    def get(self, request):
       video = Video.objects.filter(tags='剧集').order_by('-add_time')
       sort = request.GET.get('sort','')
       if sort == 'score':
           video = Video.objects.filter(tags='剧集').order_by('-click_nums')
       page = request.GET.get('page', 1)
       p = Paginator(video, 18)
       video = p.page(int(page))
       plist = p.page_range
       return render(request,'movie-list.html',{
           'video':video,
           'plist':plist,
           'sort':sort
       })
# 纪录片
class DocView(View):
    def get(self, request):
       video = Video.objects.filter(tags='纪录片').order_by('-add_time')
       sort = request.GET.get('sort','')
       if sort == 'score':
           video = Video.objects.filter(tags='纪录片').order_by('-click_nums')
       page = request.GET.get('page', 1)
       p = Paginator(video, 18)
       video = p.page(int(page))
       plist = p.page_range
       return render(request,'movie-list.html',{
           'video':video,
           'plist':plist,
           'sort':sort
       })
# 日漫
class AnimeView(View):
    def get(self, request):
       video = Video.objects.filter(tags='日漫').order_by('-add_time')
       sort = request.GET.get('sort','')
       if sort == 'score':
           video = Video.objects.filter(tags='日漫').order_by('-click_nums')
       page = request.GET.get('page', 1)
       p = Paginator(video, 18)
       video = p.page(int(page))
       plist = p.page_range
       return render(request,'movie-list.html',{
           'video':video,
           'plist':plist,
           'sort':sort
       })
# 综艺
class VarietyView(View):
    def get(self, request):
       video = Video.objects.filter(tags='综艺').order_by('-add_time')
       sort = request.GET.get('sort','')
       if sort == 'score':
           video = Video.objects.filter(tags='综艺').order_by('-click_nums')
       page = request.GET.get('page', 1)
       p = Paginator(video, 18)
       video = p.page(int(page))
       plist = p.page_range
       return render(request,'movie-list.html',{
           'video':video,
           'plist':plist,
           'sort':sort
       })
# 视频详情
class VideoDetailView(View):
    def get(self,request,video_id):
        video = Video.objects.get(id=video_id)
        comments = VideoComments.objects.filter(video=video_id)
        r_com = VideoComments.objects.all().order_by('-praise_num')[:9]
        count = comments.count()
        per_page = 2
        p = Paginator(comments, per_page)
        pages = p.num_pages
        if count > per_page:
            comments = p.page(1)
        tag = video.tags
        guess_like = Video.objects.filter(tags=tag).order_by('-click_nums')[:6]
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=video.id):
                has_fav = True
        return render(request,'movie-detail.html',{
            'video':video,
            'comments':comments,
            'has_fav':has_fav,
            'guess_like':guess_like,
            'count':count,
            'pages':pages,
            'r_com':r_com
        })
    def post(self,request,video_id):
        comments = VideoComments.objects.filter(video=video_id)
        page = request.POST.get('nex_p', 1)
        p = Paginator(comments, 2)
        comments = p.page(int(page))
        all_data = []
        for comment in comments:
            data = {}
            data['imgsrc'] = '/media/'+str(comment.user.image)
            data['nick_name'] = comment.user.nick_name
            add_time = comment.add_time
            data['add_time'] = add_time.strftime('%Y')+'年'+add_time.strftime('%m')+'月'+add_time.strftime('%d')+'日'
            data['praise_num'] = comment.praise_num
            data['comment_id'] = comment.id
            data['comment'] = mark_safe(comment.comments)
            all_data.append(data)
        all_data = {'data':all_data}
        return HttpResponse(json.dumps(all_data),content_type='application/json')
# 视频播放
class PlayView(View):
    def get(self,request,video_id):
        video = Video.objects.get(id=video_id)
        return render(request,'play.html',{
            'video':video
        })
# Create your views here.
