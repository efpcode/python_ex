from pathlib import Path
from os import environ
from distutils.util import strtobool


# Global Variable

class BabelConfy:
    """
    A class for the intial setup of a Babel project, hence the name BabelConfy
    """
    BABELHOME = Path.home()

    def __init__(self, babel_filename: str = "babel_data"):
        self.babel_filename = babel_filename

    def __repr__(self):
        return f"BabelConfy({self._babel_filename})"

    def __str__(self):
        return f"[BabelConfy(FileName)]"

    @property
    def babel_filename(self):
        print(f"Current file name...{self._babel_filename}")
        return self._babel_filename

    @babel_filename.setter
    def babel_filename(self, name: str):
        print(f"Changed name to.. {name}")
        if not(isinstance(name, str)):
            raise ValueError("Expected filename to be a string or textinput!")
        path = (self.BABELHOME / name).absolute()
        self._babel_filename = path

    def babel_mkdir(self, parents=True, exist_ok=False):
        dir_name = str(self.babel_filename)
        if dir_name[dir_name.rfind("/"):].rfind(".") > 1:
            self.babel_filename = dir_name[:dir_name.find(".")]
        return self.babel_filename.mkdir(parents=parents, exist_ok=exist_ok)

    def babel_mkfile(self, suffix=".txt", exist_ok=False):
        fname = str(self.babel_filename)
        if not (fname.count(".")):
            self.babel_filename = "".join([fname, suffix])
        return self.babel_filename.touch(exist_ok=exist_ok)


# Static Method
    @staticmethod
    def babel_fileopen(path_object=Path()):
        with path_object.open(mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                yield line

    @staticmethod
    def babel_write_to_file(mode, data, path_object=Path()):
        with path_object.open(mode=mode, encoding="utf-8") as f:
            for line in data:
                f.write(line)
            f.close()

    @staticmethod
    def _babel_configurator():
        sub_dir = BabelConfy("babel_data/.babel_config/")
        babel_config = BabelConfy("babel_data/.babel_config/babelenv.cfg")

        try:
            babel_config.babel_mkfile()

        except FileExistsError as error:
            text = f"\nConfiguration file already exists at " \
                   f"{str(babel_config.babel_filename)}.\n{error}"
            return text
        except FileNotFoundError:
            sub_dir.babel_mkdir()
            babel_config.babel_mkfile()
            return "Configuration was completed."

        else:
            return "Configuration files already exists."

    @staticmethod
    def _io_errors(func_method, cls_object):
        msg_to_user = None
        try:
            func_method()
        except FileExistsError as file_error:
            print(f"The file already exists please rename file name. File "
                  f"name conflict {file_error}")
            user_choice = strtobool(input("Do you wish to overwrite file?: "
                                          "[Y/N]"))
            if user_choice:
                print("Overwritten is only valid for files not directories.")
                return func_method(exist_ok=True)

            else:
                new_name = input("Rename file to: ")
                cls_object.babel_filename = new_name
                return func_method()

        except FileNotFoundError as file_is_not:
            print(f"The file or directory cannot be found: {file_is_not}")

            msg_to_user = "notfound.txt"
            cls_object.babel_filename = str(msg_to_user)
            return func_method()

        except AttributeError as method_miss:
            print(f"The object pass has no method called:\n{method_miss}")

        except Exception as error:
            print(f"Something else went wrong: {error}")

        return msg_to_user




class BabelCredentials:

    HOME = Path.home().joinpath("babel_data", ".babel_config", "babelenv.cfg")

    def __init__(self, data=dict(my_username=None, my_password=None)):

        self.keys = data

    def __repr__(self):
        return "BabelCredential({MY_USERNAME:username, " \
               "MY_PASSWORD:secrete_password})"

    def __str__(self):
        return "BabelCredential object has your username & password"

    def _io_exists__(self):
        return self.HOME.exists()

    def _template_parser(self, data: list):
        envars = list()
        for item in data:
            a, b, c = item.partition("=")
            tmp = a.strip("export").strip()
            key = "".join((a, b, self.keys.get(tmp.casefold()), "\n"))
            envars.append(key)
        return envars

    @property
    def keys(self):

        return dict(my_username=self.__babel_user, my_password=self.__babel_skey)

    @keys.setter
    def keys(self, data_vals):
        usr_name, password = data_vals.values()
        while True:
            cond1, cond2 = isinstance(usr_name, str), isinstance(
                password, str)
            try:
                if not (cond1 and cond2):
                    raise TypeError(f"Expected usr_name:{type(usr_name)} and "
                                    f"password {type(password)} to be "
                                    f"string typed inputs.")
            except TypeError as error:
                print(error)
                usr_name = input("Enter a valid username: ")
                password = input("Enter your password: ")
                continue
            else:
                self.__babel_user = usr_name
                self.__babel_skey = password
                break

    def credential_setup(self, override=False):
        if BabelCredentials.HOME.stat().st_size == 0 or override:
            list(BabelCredentials._template())
            data = BabelConfy.babel_fileopen(self.HOME)
            keys = self._template_parser(data)
            BabelConfy.babel_write_to_file(mode="w", data=keys, path_object=self.HOME)
            for k, v in self.keys.items():
                environ[k.upper()] = v
            return "Credentials are done!"
        else:
            new_object = BabelCredentials.user_credentials()
            self.keys = new_object.keys
            return f"Previous data entry has been loaded"

    @classmethod
    def _template(cls):
        if not(cls._io_exists__(cls)):
            raise ValueError(f"File most exists to create template: "
                             f"{str(cls.HOME)}")
        value_pairs = {"MY_USERNAME": None, "MY_PASSWORD": None,
                       "MY_APIKEY": None}
        api_file = cls.HOME

        if api_file.stat().st_size == 0:
            with api_file.open(mode="w", encoding="utf-8") as f:
                for key, value in value_pairs.items():
                    yield f.write(f"export {key}={value}\n")
        else:
            with api_file.open(mode="r", encoding="utf-8") as f:
                for line in f.readlines():
                    yield line

    @classmethod
    def user_credentials(cls):
        new_dict = dict()
        data = list(BabelConfy.babel_fileopen(cls.HOME))
        keys = [i.replace("\n", "").lstrip("export").strip()
                for i in data]
        for items in keys:
            k, v = items.split("=")
            new_dict.update({k: v})
            environ[k] = v

        keys_lower = {k.lower(): v for k, v in new_dict.items()}
        babel_object = cls(data=keys_lower)

        return babel_object
