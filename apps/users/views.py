import json
import traceback

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse, render_to_response
from django.urls import reverse
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from users.models import Banner, UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception:
            traceback.print_exc()
            return None


class IndexView(View):
    """首页"""

    def get(self, request):
        # 轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播课程
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 课程机构
        course_orgs = Course.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


class LoginView(View):
    """ 登录功能类 """

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        context = {}
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(to='/')
                context['msg'] = '用户未激活'
                return render(request, 'login.html', context)

            context['msg'] = '用户名或密码错误'
            return render(request, 'login.html', context)

        return render(request, 'login.html', context)


class RegisterView(View):
    """ 注册功能类 """

    @staticmethod
    def get(request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    @staticmethod
    def post(request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            if UserProfile.objects.filter(email=email).first():
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})

            user = UserProfile()
            user.username = email
            user.email = email
            user.password = make_password(password)
            user.is_active = False
            user.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user.id
            user_message.message = '欢迎注册幕学在线网'
            user_message.save()

            send_register_email(email, 'register')
            return redirect('/login/')

        return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    """ 用户激活类 """

    @staticmethod
    def get(request, active_code):
        all_record = models.EmailVerifyRecond.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return redirect('/login/')
        return render(request, 'active_fail.html')


class ForgetPwdView(View):
    """ 重置密码类 """

    @staticmethod
    def get(request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    @staticmethod
    def post(request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            send_status = send_register_email(email, 'forget')
            if send_status:
                return render(request, 'send_success.html')
            return HttpResponse('发送失败')
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    """ 重置密码类 """

    @staticmethod
    def get(request, active_code):
        all_record = EmailVerifyRecond.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})

        return render(request, 'active_fail.html')


class LogoutView(View):
    """用户登出"""

    @staticmethod
    def get(request):
        logout(request)
        return redirect(reverse('login'))


class ModifyView(View):
    """
    修改用户密码
    """

    @staticmethod
    def post(request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get('email')
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password=pwd1)
            user.save()
            return redirect('/login/')

        return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    @staticmethod
    def get(request):
        return render(request, 'usercenter-info.html', {})

    @staticmethod
    def post(request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            print('保存成功')
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            print('保存失败')
            print(user_info_form.errors)
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

    # def post(self, request):
    #     user_info_form = UserInfoForm(request.POST)
    #     if user_info_form.is_valid():
    #         nick_name = request.POST.get('nick_name',None)
    #         gender = request.POST.get('gender',None)
    #         birthday = request.POST.get('birthday',None)
    #         adress = request.POST.get('address',None)
    #         mobile = request.POST.get('mobile',None)
    #         user = request.user
    #         user.nick_name = nick_name
    #         user.gender = gender
    #         user.birthday = birthday
    #         user.adress = adress
    #         user.mobile = mobile
    #         user.save()
    #         return HttpResponse('{"status":"success"}', content_type='application/json')
    #     else:
    #         return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户图像修改
    """

    @staticmethod
    def post(request):
        # 上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """

    @staticmethod
    def post(request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """发送邮箱修改验证码"""

    @staticmethod
    def get(request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')

        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """修改邮箱"""

    @staticmethod
    def post(request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """我的课程"""

    @staticmethod
    def get(request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "user_courses": user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """我收藏的课程机构"""

    @staticmethod
    def get(request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """我收藏的授课讲师"""

    @staticmethod
    def get(request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """

    @staticmethod
    def get(request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    """我的消息"""

    @staticmethod
    def get(request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4, request=request)

        messages = p.page(page)
        return render(request, "usercenter-message.html", {
            "messages": messages,
        })


def page_not_found(request):
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
