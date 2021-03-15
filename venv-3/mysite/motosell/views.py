from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginUserForm, RegisterUserForm, NoticeForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from .models import Notice
from django.contrib.auth import get_user_model
import io
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.core.paginator import Paginator

# django.contrib.auth.get_user_model()

# get
def mainView(request):
    form = Notice.objects.all().filter(is_deleted=False, is_publicated=True)
    user = request.user
    paginator = Paginator(form, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'mainItem.html', {'listNotice': form, 'page_obj': page_obj, 'user': user})


@login_required()
@require_http_methods(["GET", "POST"])
def currentItem(request, pk):
    obj = Notice.objects.get(pk=pk)
    # obj = obj._meta.get_fields().values()
    user = request.user
    # print(obj)
    return render(request, 'currentItem.html', {'item': obj, 'user': user})


# get && post
def loginView(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            return render(request, 'profile/profile.html', {})
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/accounts/login/')
    else:
        form = LoginUserForm()
        return render(request, 'registration/login.html', {'form': form})


# get
def signupView(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
        return redirect('/accounts/signup/')
    else:
        form = RegisterUserForm()

    return render(request, 'registration/signup.html', {'form': form})


# @require_http_methods(["GET", "POST"])
@login_required()
def profileView(request):
    allNotice = Notice.objects.all().filter(is_deleted=False, author=request.user.id)
    user = request.user
    return render(request, 'profile/profile.html', {'user': user, 'allNoticeList': allNotice})


@login_required
def logoutView(request):
    django_logout(request)
    return HttpResponseRedirect('/')
    # logout(request)
    # return redirect('/')

@login_required
def addNoticeView(request):
    if request.user.is_authenticated:
        print('after authenticate, before POST')
        if request.method == 'POST':
            newNotice = NoticeForm(request.POST, request.FILES)
            print('###########')
            # print(newNotice)
            print('###########')
            # print(newNotice.values)
            print(request.POST)
            print(request.FILES)
            print('before valid')
            print(newNotice.is_valid())
            print(newNotice.errors.values())
            # print(formset.errors)
            if newNotice.is_valid():
                print('after valid')
                newNotice.author_id = get_user_model()
                print(newNotice)
                savedNotice = newNotice.save(commit=False)
                savedNotice.author = request.user
                savedNotice.save()
                print('success')
                return redirect('/accounts/profile/')
            else:
                print('validacja nieudana')
                # print(formset.errors)
                return redirect('/accounts/profile/')
    else:
        return redirect('/')


@login_required()
def createNoticeView(request):
    newNoticeForm = NoticeForm()
    return render(request, 'profile/noticeForm.html', {'form': newNoticeForm})


@login_required()
def download(request, pk):
    notice = Notice.objects.get(pk=pk, author=request.user.id)
    buffer = io.BytesIO()
    elem = canvas.Canvas(buffer)
    elem.drawString(100, 800, notice.title)
    elem.showPage()
    elem.save()
    # przeglądarki pozostawiają opcje zapisania
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='notice.pdf')


@login_required()
def delete(request, pk):
    if request.user.is_authenticated:
        currentNotice = Notice.objects.get(pk=pk)
        currentNotice.is_deleted = True
        currentNotice.save()
        print(currentNotice.is_deleted)
        return redirect('/accounts/profile/')
    else:
        print('niezalogowany')
        return redirect('/')


@login_required()
def updateForm(request, pk):
    if request.user.is_authenticated:
        currentNotice = Notice.objects.get(pk=pk)
        noticeFormUpdate = NoticeForm(instance=currentNotice)
        userName = request.user.get_username()
        # print(BookForm.pk)
        return render(request, 'profile/update.html',
                      {'NoticeFormUpdate': noticeFormUpdate, 'current_notice': currentNotice, 'userName': userName})
    else:
        print('użytkownik niezalogowany')
        return redirect('/')


@login_required()
def update_database(request, pk):
    currentNotice = Notice.objects.get(pk=pk)
    currentNotice.author_id = get_user_model()
    print('dziala ', currentNotice)
    updatedNotice = NoticeForm(instance=currentNotice)
    # if book.is_valid():
    updatedNotice = NoticeForm(request.POST, instance=currentNotice)
    updatedNotice.save()
    return redirect('/accounts/profile/')


@login_required()
def publicated(request, pk):
    if request.user.is_authenticated:
        noticeObj = Notice.objects.get(pk=pk)
        noticeObj.is_publicated = True
        noticeObj.save()
        return redirect('/accounts/profile/')
