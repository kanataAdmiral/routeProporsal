class LoginException(Exception):
    def __str__(self):
        return "ユーザIDが登録されていない、またはパスワードが正しくありません。"


class PointException(Exception):
    def __str__(self):
        return "出入口が田んぼの中に存在していない、または田んぼの線上にあるため、田んぼの中に描画してください。"
