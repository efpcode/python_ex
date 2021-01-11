from os import environ
from requests import request

class BabelClient:
    def __init__(self):
        pass



    def login_fields(self):
        stem = "https://api.mymemory.translated.net/keygen?"
        web_cred = ("user=", "&pass=")
        user_data = BabelClient.get_usr_data()
        login_data = ["".join(i) for i in list(zip(web_cred, user_data))]

        return "".join((stem,"".join(login_data)))

    def test_connection(self):
        call = self.login_fields()
        response = request("GET",call)
        return response

    #static methods
    @staticmethod
    def get_usr_data():
        return (environ.get("MY_USERNAME"), environ.get("MY_PASSWORD"))