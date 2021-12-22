import hashlib
from ..models import User
from ..exception import Exception


salt = bytes("b'pelob/9gQSxIsZ66wlu+wblqY8wuqT0HQl7TODMotyA='", 'utf-8')


def get_digest(password):
    password = bytes(password, 'utf-8')
    digest = hashlib.sha256(salt + password).hexdigest()
    for _ in range(10000):
        digest = hashlib.sha256(bytes(digest, 'utf-8')).hexdigest()
    return digest


def login_check(user_id, loginPass):
    loginPass = get_digest(loginPass)
    try:
        matchUser = User.objects.get(id=user_id)
        if matchUser.password == loginPass:
            return True
        else:
            raise Exception.LoginException('パスワードが違います')
    except User.DoesNotExist:
        raise Exception.LoginException('ユーザが見つかりません')
