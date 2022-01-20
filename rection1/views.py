from django.shortcuts import render
from django.http import HttpResponse
from . import form
from .paddy.util import util
from .exception import Exception
from rection1.paddy.Repository.paddyRepository import PaddyParameter, StartEndPosition
from .paddy.paddyproperty import PaddyProperty
from rection1.paddy.Repository.machineRepository import Machine
import time


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
        start = time.time()
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
            # print(p.moveList.to_json(indent=4, ensure_ascii=False))
            elapsed_time = time.time() - start
            print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
        except Exception.PointException as e:
            return HttpResponse(e)
        return HttpResponse(p.moveList.to_json(indent=4, ensure_ascii=False))
    else:
        return HttpResponse("違うメソッドを使用しています。")
