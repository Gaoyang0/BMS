from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from utils.paging import Page
from utils import analysis_query
from app import models
from app.models import Books
import os, json, time, datetime
from utils.writeLog import log


# Create your views here.


class Index(View):

    def dispatch(self, request, *args, **kwargs):
        print("before")  # 此处可在请求前做一些操作
        result = super(Index, self).dispatch(request, *args, **kwargs)
        print('after')  # 此处可在请求后做一些操作
        return result

    def get(self, request):
        current_page = int(request.GET.get('p', default=1))
        data_count = models.Books.objects.all().__len__()
        page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=10)
        books = models.Books.objects.all()[page_obj.start:page_obj.end]
        page_str = page_obj.page_str('/app/index')
        news = models.News.objects.all()[0:5].values('nid', 'ntitle')
        hupic = getupic(request)
        return render(request, 'index.html', {'hupic': hupic, 'books': books, 'page_str': page_str, 'news': news})


# 管理图书
class ManageBook(View):

    def get(self, request):
        if checklogin(request) and checkpower(request):
            current_page = int(request.GET.get('p', default=1))
            data_count = models.Books.objects.all().__len__()
            page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=10)
            books = models.Books.objects.all()[page_obj.start:page_obj.end]
            for item in books:
                item.fabulous = models.AddFabulous.objects.filter(b_id=item.bid).all().count()
            page_str = page_obj.page_str('/app/manage-book')
            hupic = getupic(request)
            return render(request, 'manage-book.html', {'hupic': hupic, 'books': books, 'page_str': page_str})
        else:
            return redirect('/app/login/')


# 插入图书
class InsertBook(View):

    def get(self, request):
        if checklogin(request) and checkpower(request):
            hupic = getupic(request)
            family = ['哲学', '经济学', '法学', '教育学', '文学', '历史学', '理学', '工学', '农学', '医学', '军事学', '管理学']
            return render(request, 'insert-book.html', {'hupic': hupic, "family": family})
        else:
            return redirect('/app/login/')

    def post(self, request):
        if checklogin(request) and checkpower(request):
            bid = request.POST.get('bid')
            bname = request.POST.get('bname')
            bprice = request.POST.get('bprice')
            bstock = request.POST.get('bstock')
            bfamily = request.POST.get('bfamily')

            file_obj = request.FILES.get('bpic')
            file_path = os.path.join('static/data', bid + '.png')
            f = open(file_path, mode='wb')
            for item in file_obj.chunks():
                f.write(item)
            f.close()
            bpic = '/static/data/' + bid + '.png'
            models.Books.objects.create(bid=bid, bname=bname, bprice=bprice, bstock=bstock, bfamily=bfamily, bpic=bpic)
            dic = {'bid': bid, "bname": bname, "bprice": bprice, "bstock": bstock, "bfamily": bfamily, "bpic": bpic}
            str = '插入一条图书记录:' + json.dumps(dic)
            print(str)
            log(str, 'book')
            return redirect('/app/manage-book/')
        else:
            return redirect('/app/login/')


# 删除图书
def deleteBook(request):
    if checklogin(request) and checkpower(request):
        bid = request.GET.get('bid')
        models.Books.objects.filter(bid=request.GET.get('bid')).delete()
        str = '删除一条ID为:' + bid + '图书记录'
        print(str)
        log(str, 'book')
        try:
            os.remove('static/data/' + bid + '.png')
        except Exception as e:
            print('对应的图片有可能不存在')
        return redirect('/app/manage-book/')
    else:
        return redirect('/app/login/')


class ModifyBook(View):

    def get(self, request):
        if checklogin(request) and checkpower(request):
            bid = request.GET.get('bid')
            res = models.Books.objects.filter(bid=bid).first()
            family = ['哲学', '经济学', '法学', '教育学', '文学', '历史学', '理学', '工学', '农学', '医学', '军事学', '管理学']
            hupic = getupic(request)
            return render(request, "modify-book.html",
                          {'hupic': hupic, "family": family, 'bid': res.bid, "bname": res.bname, "bprice": res.bprice,
                           'bstock': res.bstock, "bfamily": res.bfamily})
        else:
            return redirect('/app/login/')

    def post(self, request):
        if checklogin(request) and checkpower(request):
            bid = request.POST.get('bid')
            bname = request.POST.get('bname')
            bprice = request.POST.get('bprice')
            bstock = request.POST.get('bstock')
            bfamily = request.POST.get('bfamily')

            file_obj = request.FILES.get('bpic')
            file_path = os.path.join('static/data', bid + '.png')
            f = open(file_path, mode='wb')
            for item in file_obj.chunks():
                f.write(item)
            f.close()
            bpic = '/static/data/' + bid + '.png'
            models.Books.objects.filter(bid=bid).update(bname=bname, bprice=bprice, bstock=bstock, bfamily=bfamily,
                                                        bpic=bpic)
            dic = {'bid': bid, "bname": bname, "bprice": bprice, "bstock": bstock, "bfamily": bfamily, "bpic": bpic}
            str = '修改一条图书记录:' + json.dumps(dic)
            print(str)
            log(str, 'book')
            return redirect('/app/manage-book/')
        else:
            return redirect('/app/login/')


# 管理用户
class ManageUser(View):

    def get(self, request):
        if checklogin(request) and checkpower(request):
            current_page = int(request.GET.get('p', default=1))
            data_count = models.Users.objects.all().__len__()
            page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=10)
            users = models.Users.objects.all()[page_obj.start:page_obj.end]
            page_str = page_obj.page_str('/app/manage-user')
            hupic = getupic(request)
            return render(request, 'manage-user.html', {'hupic': hupic, 'users': users, 'page_str': page_str})
        else:
            return redirect('/app/login/')


# 插入用户
class InsertUser(View):

    def get(self, request):
        if checklogin(request) and checkpower(request):
            role = ['管理员', '用户']
            hupic = getupic(request)
            return render(request, 'insert-user.html', {"hupic": hupic, "role": role})
        else:
            return redirect('/app/login/')

    def post(self, request):
        if checklogin(request) and checkpower(request):
            uid = request.POST.get('uid')
            uname = request.POST.get('uname')
            utel = request.POST.get('utel')
            upwd = request.POST.get('upwd')
            urole = request.POST.get('urole', None)
            file_obj = request.FILES.get('upic')
            file_path = os.path.join('static/data', uid + '.png')
            f = open(file_path, mode='wb')
            for item in file_obj.chunks():
                f.write(item)
            f.close()
            upic = '/static/data/' + uid + '.png'
            models.Users.objects.create(uid=uid, uname=uname, utel=utel, upwd=upwd, urole=urole, upic=upic)
            dic = {'uid': uid, "uname": uname, "utel": utel, "upwd": upwd, "urole": urole, "upic": upic}
            str = '插入一条用户记录:' + json.dumps(dic)
            print(str)
            log(str, 'user')
            return redirect('/app/manage-user/')
        else:
            return redirect('/app/login/')


# 删除用户
def deleteUser(request):
    if checklogin(request) and checkpower(request):
        uid = request.GET.get('uid')
        print(uid)
        models.Users.objects.filter(uid=uid).delete()
        str = '删除一条ID为:' + uid + '用户记录'
        print(str)
        log(str, 'user')
        try:
            os.remove('static/data/' + uid + '.png')
        except Exception as e:
            print('对应的图片有可能不存在')
        return redirect('/app/manage-user/')
    else:
        return redirect('/app/login/')


class ModifyUser(View):
    def get(self, request):
        if checklogin(request) and checkpower(request):
            uid = request.GET.get('uid')
            res = models.Users.objects.filter(uid=uid).first()
            role = ['管理员', '用户']
            hupic = getupic(request)
            return render(request, "modify-user.html",
                          {"hupic": hupic, "role": role, 'uid': res.uid, "uname": res.uname, "utel": res.utel,
                           'urole': res.urole, 'upwd': res.upwd})
        else:
            return redirect('/app/login/')

    def post(self, request):
        if checklogin(request) and checkpower(request):
            uid = request.POST.get('uid')
            uname = request.POST.get('uname')
            utel = request.POST.get('utel')
            upwd = request.POST.get('upwd')
            urole = request.POST.get('urole')

            file_obj = request.FILES.get('upic')
            file_path = os.path.join('static/data', uid + '.png')
            f = open(file_path, mode='wb')
            for item in file_obj.chunks():
                f.write(item)
            f.close()
            upic = '/static/data/' + uid + '.png'
            models.Users.objects.filter(uid=uid).update(uname=uname, utel=utel, upwd=upwd, urole=urole, upic=upic)
            dic = {'uid': uid, "uname": uname, "utel": utel, "upwd": upwd, "urole": urole, "upic": upic}
            str = '修改一条用户记录:' + json.dumps(dic)
            print(str)
            log(str, 'user')
            return redirect('/app/manage-user/')
        else:
            return redirect('/app/login/')


# 管理新闻
class ManageNew(View):

    def get(self, request):
        if checklogin(request) and checkpower(request):
            current_page = int(request.GET.get('p', default=1))
            data_count = models.News.objects.all().__len__()
            page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=10)
            news = models.News.objects.all()[page_obj.start:page_obj.end]
            page_str = page_obj.page_str('/app/manage-new')
            hupic = getupic(request)
            return render(request, 'manage-new.html', {'hupic': hupic, 'news': news, 'page_str': page_str})
        else:
            return redirect('/app/login/')


# 插入新闻
class InsertNew(View):

    def get(self, request):
        if checklogin(request) and checkpower(request):
            family = ['军事', '体育', '外交', '其他']
            hupic = getupic(request)
            return render(request, 'insert-new.html', {'hupic': hupic, "family": family})
        else:
            redirect('/app/login/')

    def post(self, request):
        if checklogin(request) and checkpower(request):
            ntitle = request.POST.get('ntitle')
            ncontent = request.POST.get('ncontent')
            nfamily = request.POST.get('nfamily')
            time_now = datetime.datetime.now()
            print(ntitle, ncontent, nfamily, time_now)
            models.News.objects.create(ndate_create=time_now, ntitle=ntitle, ncontent=ncontent, nfamily=nfamily)
            return redirect('/app/manage-new/')
        else:
            return redirect('/app/login/')


# 删除新闻
def deleteNew(request):
    if checklogin(request) and checkpower(request):
        nid = request.GET.get('nid')
        models.News.objects.filter(nid=nid).delete()
        return redirect('/app/manage-new/')
    else:
        return redirect('/app/login/')


# 检查图书ID
def checkbid(request):
    if models.Books.objects.filter(bid=request.GET.get('bid')).count() == 0:
        result = {'getdata': 'true'}
    else:
        result = {'getdata': 'false'}
    return HttpResponse(json.dumps(result))


# 检查用户ID
def checkuid(request):
    if models.Users.objects.filter(uid=request.GET.get('uid')).count() == 0:
        result = {'getdata': 'true'}
    else:
        result = {'getdata': 'false'}
    return HttpResponse(json.dumps(result))


from django.utils.safestring import mark_safe


def showNews(request):
    nid = request.GET.get('nid')
    res = models.News.objects.filter(nid=nid).first()
    ncontent = mark_safe("".join(res.ncontent))
    return render(request, 'show-news.html', {'ntitle': res.ntitle, 'ncontent': ncontent})


def query(request):
    flag = request.GET.get('flag')
    if flag == 'book':
        current_page = int(request.GET.get('p', default=1))
        keyword = request.GET.get('keyword', None)
        limit = analysis_query.query_book(keyword)
        data_count = models.Books.objects.filter(Q(bid__contains=limit['id']) | Q(bname__contains=limit['name']) | Q(
            bfamily__contains=limit['family'])).__len__()
        print(data_count)
        from utils.paging1 import Page as Page1
        page_obj = Page1(current_page=current_page, data_count=data_count, per_page_count=10)
        books = models.Books.objects.filter(
            Q(bid__contains=limit['id']) | Q(bname__contains=limit['name']) | Q(bfamily__contains=limit['family']))[
                page_obj.start:page_obj.end]
        page_str = page_obj.page_str('/app/query?flag=book&keyword=' + keyword)
    news = models.News.objects.all()[0:5].values('nid', 'ntitle')
    hupic = getupic(request)
    return render(request, 'index.html', {'hupic': hupic, 'books': books, 'page_str': page_str, 'news': news})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        u = request.POST.get('username', None)
        p = request.POST.get('password', None)
        if u and p:
            res = models.Users.objects.filter(uid=u, upwd=p).first()
            if res:
                if res.urole == '管理员':
                    request.session['uid'] = u
                    request.session['is_login'] = True
                    request.session['power'] = True
                    request.session.set_expiry(60 * 10)
                    return redirect('/app/manage-book')
                elif res.urole == '用户':
                    request.session['uid'] = u
                    request.session['is_login'] = True
                    request.session['power'] = False
                    request.session.set_expiry(60 * 10)
                    return redirect('/app/index')
                else:
                    return render(request, 'login.html', {'error': '用户名或密码错误'})
            else:
                return render(request, 'login.html', {'error': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'error': '用户名或密码不能为空'})


def logout(request):
    request.session.clear()
    return redirect('/app/login/')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        uid = request.POST.get('uid')
        uname = request.POST.get('uname')
        utel = request.POST.get('utel')
        upwd = request.POST.get('upwd')
        urole = request.POST.get('urole', None)
        if urole == None:
            urole = '用户'
        file_obj = request.FILES.get('upic')
        file_path = os.path.join('static/data', uid + '.png')
        f = open(file_path, mode='wb')
        for item in file_obj.chunks():
            f.write(item)
        f.close()
        upic = '/static/data/' + uid + '.png'
        models.Users.objects.create(uid=uid, uname=uname, utel=utel, upwd=upwd, urole=urole, upic=upic)
        dic = {'uid': uid, "uname": uname, "utel": utel, "upwd": upwd, "urole": urole, "upic": upic}
        str = '插入一条用户记录:' + json.dumps(dic)
        print(str)
        log(str, 'user')
        return redirect('/app/login/')


def borrowbook(request):
    if checklogin(request):
        bid = request.GET.get('bid', None)
        uid = request.session.get('uid', None)
        print(bid)
        res = models.Books.objects.filter(bid=bid).first()
        print(res)
        if res.bstock:
            models.BorrowBooks.objects.create(b_id=bid, u_id=uid)
            b = models.Books.objects.filter(bid=bid).first()
            models.Books.objects.filter(bid=bid).update(bstock=int(b.bstock) -  1)
        else:
            print("库存不够")
        print(bid, uid)
    else:
        return redirect('/app/login')
    return redirect('/app/index')


def checklogin(request):
    if request.session.get('is_login', None):
        return True
    else:
        return False


def checkpower(request):
    if request.session.get('power', None):
        return True
    else:
        return False


def zan(request):
    if checklogin(request):
        bid = request.GET.get('bid', None)
        uid = request.session.get('uid', None)
        res = models.AddFabulous.objects.filter(b_id=bid, u_id=uid).first()
        if res:
            print("不能重复点赞")
        else:
            models.AddFabulous.objects.create(b_id=bid, u_id=uid, flag=1)
    else:
        return redirect('/app/login')
    return redirect('/app/index')


def cai(request):
    if checklogin(request):
        bid = request.GET.get('bid', None)
        uid = request.session.get('uid', None)
        res = models.AddFabulous.objects.filter(b_id=bid, u_id=uid).first()
        if res:
            print("不能重复点踩")
        else:
            models.AddFabulous.objects.create(b_id=bid, u_id=uid, flag=0)
    else:
        return redirect('/app/login')
    return redirect('/app/index')


def getupic(request):
    hupic = '/static/images/huaji.png'
    if checklogin(request):
        hupic = models.Users.objects.filter(uid=request.session.get('uid', None))
        if hupic is not None:
            hupic = hupic[0].upic
    return hupic


def recommend(request):
    current_page = int(request.GET.get('p', default=1))
    books = models.Books.objects.all()
    for item in books:
        item.fabulous = models.AddFabulous.objects.filter(b_id=item.bid).all().count()
    b = []
    for item in books:
        if item.fabulous > 2 and b.__len__() < 10:
            b.append(item)
        else:
            continue
    hupic = getupic(request)
    return render(request, 'index.html', {'hupic': hupic, 'books': b})

def bb(request):
    if checklogin(request) and checkpower(request):
        current_page = int(request.GET.get('p', default=1))
        data_count = models.BorrowBooks.objects.all().count()
        page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=10)
        bbs = models.BorrowBooks.objects.all()[page_obj.start:page_obj.end]
        page_str = page_obj.page_str('/app/manage-bb')
        hupic = getupic(request)
        return render(request, 'manage-bb.html', {'hupic': hupic, 'bbs': bbs, 'page_str': page_str})
    else:
        return redirect('/app/login/')

def delbb(request):
    if checklogin(request) and checkpower(request):
        bid = request.GET.get('bid', None)
        uid = request.GET.get('uid', None)
        res = models.BorrowBooks.objects.filter(b_id=bid, u_id=uid).first()
        if res:
            models.BorrowBooks.objects.filter(b_id=bid, u_id=uid).first().delete()
            b = models.Books.objects.filter(bid=bid).first()
            models.Books.objects.filter(bid=bid).update(bstock=int(b.bstock)+1)
        else:
            print('未借此书')
        print(bid, uid)
    else:
        return redirect('/app/login')
    return redirect('/app/manage-bb')

