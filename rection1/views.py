from django.shortcuts import render
from django.http import HttpResponse
from . import form
from .util import util
from .exception import Exception
from rection1.paddy.Model.paddyModel import PaddyParameter, StartEndPosition
from .paddy.paddyproperty import PaddyProperty
from rection1.paddy.Model.machineModel import Machine


def login(request):
    if request.method == 'POST':
        newUser = form.SignUpForm(request.POST or None)
        password = request.POST['password']
        if newUser.is_valid():
            user = newUser.save(commit=False)
            user.password = util.get_digest(password=password)
            user.save()
            loginForm = form.LoginForm()
            return render(request, 'login.html', {'loginForm': loginForm})
        else:
            return HttpResponse("newUser in not valid")
    else:
        loginForm = form.LoginForm()
    return render(request, 'login.html', {'loginForm': loginForm})


def signUp(request):
    signUpForm = form.SignUpForm()
    return render(request, 'signup.html', {"signUpForm": signUpForm})


def loginConf(request):
    if request.method == 'POST':
        loginInfo = form.LoginForm(request.POST)
        id = request.POST['id']
        password = request.POST['password']
        if loginInfo.is_valid():
            try:
                util.login_check(id, password)
            except Exception.LoginException as e:
                return HttpResponse(e)
            return render(request, 'paddy_field.html')
    else:
        return HttpResponse("違うメソッドを使用しています。")


def position(request):
    if request.method == 'GET':
        # JSON情報を取得
        pram = request.GET.get("location_json_data")
        start_end_point = request.GET.get("location_start_end_point_data")

        if pram is None:
            return HttpResponse("田んぼの範囲を指定してください")
        if start_end_point is None:
            return HttpResponse("出入り口を指定してください")

        # 受け取った値をJSONに整形
        paddyFields: PaddyParameter = PaddyParameter.from_json(pram)
        startEndPointInfo: StartEndPosition = StartEndPosition.from_json(start_end_point)
        machineInfo = Machine(plant=6, length=3320, width=1920)

        try:
            p = PaddyProperty(paddyFields.paddyFields, startEndPointInfo.startEndPosition, machineInfo)
        except Exception.PointException as e:
            return HttpResponse(e)
        return HttpResponse(p.paddyDistance)
    else:
        return HttpResponse("違うメソッドを使用しています。")
