class LoginException(Exception):
    def __str__(self):
        return "ユーザIDが登録されていない、またはパスワードが正しくありません。"
