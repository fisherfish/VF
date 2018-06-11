from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import HttpResponse

from .models import UserProfile, EmailVerifyRecord,Banner
from videos.models import Video
from .forms import LoginForm,RegisterForm,ForgetForm,ResetPwdForm,ChangePwdForm,UserInfoForm,ImageUploadForm
from operation.models import UserMessage,UserFavorite,VideoComments
from utils import email_send
from utils.mixin_utils import LoginRequeredMixin

# 首页
class IndexView(View):
    def get(self,request):
        banners = Banner.objects.all().order_by('index')[:3]
        movie = Video.objects.filter(tags='电影').order_by('-add_time')[:10]
        tv = Video.objects.filter(tags='剧集').order_by('-add_time')[:10]
        anime = Video.objects.filter(tags='日漫').order_by('-add_time')[:10]
        doc = Video.objects.filter(tags='纪录片').order_by('-add_time')[:10]
        variety = Video.objects.filter(tags='综艺').order_by('-add_time')[:10]
        movie2 = Video.objects.filter(tags='电影').order_by('-click_nums')[:8]
        tv2 = Video.objects.filter(tags='剧集').order_by('-click_nums')[:8]
        anime2 = Video.objects.filter(tags='日漫').order_by('-click_nums')[:8]
        doc2 = Video.objects.filter(tags='纪录片').order_by('-click_nums')[:8]
        variety2 = Video.objects.filter(tags='综艺').order_by('-click_nums')[:8]
        return render(request,'index.html',{
            'banners':banners,
            'movie':movie,'tv':tv,'anime':anime,'doc':doc,'variety':variety,
            'movie2': movie2,'tv2': tv2,'anime2': anime2,'doc2': doc2,'variety2': variety2
        })

# 登录
class LoginView(View):
    def get(self,request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form':login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('pwd', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return render(request, 'login.html', {'msg': '用户未激活','login_form':login_form})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误','login_form':login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})

# 登出
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('/')

#注册
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html')
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('username', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html',{'msg':'用户已注册','register_form':register_form})
            pass_word = request.POST.get('pwd', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()

            user_massage = UserMessage()
            user_massage.user = user_profile.id
            user_massage.Message = '欢迎注册VF视界'
            user_massage.save()

            email_send.send_register_email(user_name, 'register')
            return redirect('/login/')
        else:
            return render(request, 'register.html',{'register_form':register_form})

# 邮箱激活
class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

                user_message = UserMessage()
                user_message.Message = '账号激活成功'
                user_message.user = user.id
                user_message.save()
        else:
            return render(request, 'register.html',{'msg':'激活失败'})
        return redirect('/login/')

#自定义authenticate,登录验证
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except:
            return None

# 发送邮箱验证码找回密码
class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm
        return render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('username','')
            email_send.send_register_email(email,'forgetpwd')
            return render(request, 'forgetpwd.html',{'msg':'发送成功'})
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

# 重置密码(邮箱)
class ResetPwdView(View):
    # 邮箱验证码验证
    def get(self,request,reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                return render(request,'pwdrst.html')
        else:
            return render(request, 'forgetpwd.html',{'msg':'无效链接'})
        return render(request, 'login.html')
class ModifyPwdView(View):
    # 重置密码
    def post(self,request):
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            pwd = request.POST.get('pwd','')
            email = request.POST.get('username','')
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd)
            user.save()
            return redirect('/login/')
        else:
            return render(request,'pwdrst.html',{'reset_pwd_form':reset_pwd_form})

# 用户信息展示
class UserInfoView(LoginRequeredMixin,View):
    def get(self, request):
        return render(request, 'user-detail.html')

    def post(self, request):
        user_info_form = UserInfoForm(request.POST)
        print(user_info_form.errors)
        if user_info_form.is_valid():
            address = request.POST.get('address','')
            name = request.POST.get('name','')
            gender = request.POST.get('gender','')
            user = request.user
            user.address = address
            user.gender = gender
            user.nick_name = name
            user.save()
            return render(request,'user-detail.html')
        else:
            return render(request,'user-detail.html')

# 个人中心重置密码
class ChangePwdView(LoginRequeredMixin,View):
    # 重置密码
    def post(self,request):
        reset_pwd_form = ChangePwdForm(request.POST)
        if reset_pwd_form.is_valid():
            pwd = request.POST.get('pwd','')
            user = request.user
            user.password = make_password(pwd)
            user.save()
            return redirect('/login/')
        else:
            return render(request,'pwdrst.html',{'reset_pwd_form':reset_pwd_form})
# 个人中心修改头像
class UpLoadImageView(LoginRequeredMixin,View):
    def post(self,request):
        image_form = ImageUploadForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return redirect('/user/info/')
        else:
            return HttpResponse('{"status":"fail"}',content_type='application/json')

# 我的评论
class UserCommentView(LoginRequeredMixin,View):
    def get(self, request):
        u_com = VideoComments.objects.filter(user=request.user)
        page = request.GET.get('page', 1)
        p = Paginator(u_com, 6)
        u_com = p.page(int(page))
        plist = p.page_range
        return render(request, 'user-comment.html',{'u_com':u_com,'plist':plist})
    def post(self,request):
        comment_id = request.POST.get('comment_id','')
        comment = VideoComments.objects.filter(id=comment_id)
        comment.delete()
        return HttpResponse('')
# 我的收藏
class UserFavView(LoginRequeredMixin,View):
    def get(self, request):
        user = request.user
        user_fav = UserFavorite.objects.filter(user=user.id)
        page = request.GET.get('page', 1)
        p = Paginator(user_fav, 8)
        user_fav = p.page(int(page))
        plist = p.page_range
        videos = []
        for fav in user_fav:
            video_id = fav.fav_id
            video = Video.objects.get(id=video_id)
            videos.append(video)
        return render(request, 'user-fav.html',{
            'videos':videos,
            'plist':plist,
            'user_fav':user_fav
        })
# Create your views here.
