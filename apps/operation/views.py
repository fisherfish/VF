from datetime import datetime

from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.http import HttpResponse

from .models import UserFavorite,VideoComments
from videos.models import Video
from operation.models import CommentsPraise
from utils.mixin_utils import LoginRequeredMixin

# 留言版
class BoardView(View):
    def get(self,request):
        return render(request,'msg-board.html')
    def post(self,request):
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address','')
        msg = request.POST.get('message','')
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg_all = '时间：'+dt+'\n称谓：'+name+'\n邮箱：'+email+'\n地址：'+address+'\n留言：'+msg+'\n\n'
        f = open('msg_board','a+')
        f.write(msg_all)
        f.close()
        return redirect('/')

# 检索
class SearchView(View):
    def post(self,request):
        name = request.POST.get('name','')
        if name:
            video = Video.objects.filter(name__icontains=name)
            if video.count() == 1:
                video = video.first()
                url = '/'+'video'+'/'+'detail'+'/'+str(video.id)+'/'
                return redirect(url)
            return render(request,'search-list.html',{'video':video})
        return HttpResponse('搜索出错')

# 添加收藏
class AddFavView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            # 判断用户是否登录
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')
        fav_id = request.POST.get('fav_id',0)
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id))
        if exist_records:
            exist_records.delete()
            video = Video.objects.get(id=int(fav_id))
            video.fav_nums -= 1
            if video.fav_nums < 0:
                video.fav_nums = 0
            video.save()
            return HttpResponse('{"status":"success","msg":"fav"}',content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id)>0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.save()
                video = Video.objects.get(id=int(fav_id))
                video.fav_nums += 1
                video.save()
                return HttpResponse('{"status":"success","msg":"already"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}',content_type='application/json')

# 添加评论
class AddCommentView(LoginRequeredMixin,View):
    def post(self,request):
        video_comment = VideoComments()
        video_comment.user = request.user
        video_comment.video_id= request.POST.get('video_id','')
        video_comment.comments_title = request.POST.get('comment_title','')
        video_comment.comments = request.POST.get('hcontent','')
        video_comment.save()
        return redirect('/video/detail/%s/#comment-item'%video_comment.video_id)

# 点赞评论
class CommentPraiseView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            # 判断用户是否登录
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')
        parise_id = request.POST.get('praise_id',0)
        exist_records = CommentsPraise.objects.filter(user=request.user,comment_id=int(parise_id))
        if exist_records:
            exist_records.delete()
            comment = VideoComments.objects.get(id=int(parise_id))
            comment.praise_num -= 1
            if comment.praise_num < 0:
                comment.praise_num = 0
            comment.save()
            return HttpResponse('{"status":"success","msg":"praise","praise_num":%s}'%comment.praise_num,content_type='application/json')
        else:
            commentpraise = CommentsPraise()
            if int(parise_id)>0:
                commentpraise.user = request.user
                commentpraise.comment_id = int(parise_id)
                commentpraise.save()
                comment = VideoComments.objects.get(id=int(parise_id))
                comment.praise_num += 1
                comment.save()
                return HttpResponse('{"status":"success","msg":"already","praise_num":%s}'%comment.praise_num, content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"点赞出错"}',content_type='application/json')

# 404页面
def page_notfound(request):
    from django.shortcuts import render_to_response
    responds = render_to_response('404.html',{})
    responds.status_code = 404
    return responds
# 500页面
def page_error():
    from django.shortcuts import render_to_response
    responds = render_to_response('500.html',{})
    responds.status_code = 500
    return responds
# Create your views here.
