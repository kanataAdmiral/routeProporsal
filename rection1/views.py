from django.shortcuts import render
from django.http import HttpResponse
from . import form
from .util import util
from .exception import Exception
from .paddy import paddy as pp
from .paddy.parameter import PaddyParameter
from .paddy.paddyproperty import PaddyProperty
from .paddy.parameter import StartEndPosition


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

        p = PaddyProperty(paddyFields.paddyFields, startEndPointInfo)
        # print(*p.paddyArray, sep="\n")
        # print("縦の長さ", p.vertical)
        # print("横の長さ", p.beside)
        # print("nodeList", *p.nodeList, sep="\n")
        # print("topToEndNode", p.topToEndNode)
        # print("ポジションの距離")
        # print("上", p.topIndex)
        # print("下", p.bottomIndex)
        # print("右", p.rightIndex)
        # print("左", p.leftIndex)
        # print(*p.paddyDistance, sep="\n")
        # print("始点終点の情報", p.startEndPosition)
        return HttpResponse(p.paddyDistance)
    else:
        return HttpResponse("違うメソッドを使用しています。")
