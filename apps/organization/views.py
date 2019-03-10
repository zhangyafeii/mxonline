import json

from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from operation.models import UserFavorite
from organization.forms import UserAskForm
from organization.models import CourseOrg, CityDict, Teacher


class OrgView(View):
    """
    课程机构列表功能
    """

    @staticmethod
    def get(request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        keyword_type = request.GET.get('type', "")
        # 城市列表
        all_citys = CityDict.objects.all()
        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)
        print(keyword_type)
        context = {
            'all_orgs': orgs, 'all_citys': all_citys, 'sort': sort,
            'org_nums': org_nums, 'city_id': city_id,
            'category': category, 'hot_orgs': hot_orgs,
            'category_choice': CourseOrg.category_choices,
            'keywords': search_keywords,
            'keyword_type': keyword_type,
        }

        return render(request, 'org-list.html', context=context)


class AddUserAskView(View):
    """
    用户添加咨询
    """

    @staticmethod
    @csrf_exempt
    def post(request):
        resp = {'status': 'success'}
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse(json.dumps(resp, ensure_ascii=False))
        else:
            resp['status'] = 'fail'
            resp['msg'] = '添加出错'
            return HttpResponse(json.dumps(resp, ensure_ascii=False))


class OrgHomeView(View):
    """
    机构首页
    """

    @staticmethod
    def get(request, org_id):
        print(org_id, type(org_id))
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=org_id)
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]

        context = {'all_courses': all_courses, 'all_teachers': all_teachers,
                   'course_org': course_org, 'current_page': current_page,
                   'org_id': org_id,
                   }
        return render(request, 'org-detail-homepage.html', context)


class OrgCoueseView(View):
    """
    机构课程列表页
    """
    @staticmethod
    def get(request, org_id):
        print(org_id, type(org_id))
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=org_id)
        all_courses = course_org.course_set.all()[:3]
        context = {'all_courses': all_courses, 'course_org': course_org,
                   'current_page': current_page,
                   }
        return render(request, 'org-detail-course.html', context)


class OrgDescView(View):
    """
    机构介绍页
    """
    @staticmethod
    def get(request, org_id):
        print(org_id, type(org_id))
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=org_id)
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        context = {'course_org': course_org, 'current_page': current_page, 'has_fav': has_fav}
        return render(request, 'org-detail-desc.html', context)


class OrgTeacherView(View):
    """
    机构教师页
    """
    @staticmethod
    def get(request, org_id):
        print(org_id, type(org_id))
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=org_id)
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        context = {'all_teachers': all_teachers, 'course_org': course_org,
                   'current_page': current_page, 'has_fav': has_fav}
        return render(request, 'org-detail-teachers.html', context)


class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """
    @staticmethod
    def post(request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表页
    """
    @staticmethod
    def get(request):
        all_teachers = Teacher.objects.all()
        keyword_type = request.GET.get('type', "")
        # 课程讲师搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords) |
                                               Q(work_position__icontains=search_keywords))

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)

        context = {
            "all_teachers": teachers, "sorted_teacher": sorted_teacher,
            "sort": sort, 'keywords': search_keywords, 'keyword_type': keyword_type,
            }

        return render(request, "teachers-list.html", context=context)


class TeacherDetailView(View):
    """
    教师详情
    """
    @staticmethod
    def get(request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_teacher_faved = True

        has_org_faved = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                has_org_faved = True

        # 讲师排行
        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        context = {
            "teacher": teacher, "all_courses": all_courses, "sorted_teacher": sorted_teacher,
            "has_teacher_faved": has_teacher_faved, "has_org_faved": has_org_faved,
            }
        return render(request, "teacher-detail.html", context=context)
