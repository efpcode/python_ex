from os import environ
from requests import request

class BabelClient:
    def __init__(self):
        pass
    def __str__(self):
        return "BabelClient.APICaller"

    def __repr__(self):
        return "BabelClient.Response[GET, POST]"

    def login_fields(self):
        stem = "https://api.mymemory.translated.net/keygen?"
        web_cred = ("user=", "&pass=")
        user_data = BabelClient.get_usr_data()
        login_data = ["".join(i) for i in list(zip(web_cred, user_data))]

        return "".join((stem,"".join(login_data)))

    def test_connection(self):
        call = self.login_fields()
        response = request("GET", call)
        if not response.ok:
            return f"User was not able to contact mymemory client because " \
                   f"of error \n: {response.reason}"

        environ["MY_APIKEY"] = "".join(eval(response.text).values())
        return response

    #static methods
    @staticmethod
    def get_usr_data():
        return (environ.get("MY_USERNAME"), environ.get("MY_PASSWORD"))
