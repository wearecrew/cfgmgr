"""
Config loader
"""

import json
import os
from json.decoder import JSONDecodeError

from cryptography.fernet import Fernet


class MissingProjectFile(Exception):
    """Missing project file exception"""


class MissingMasterKey(Exception):
    """Missing master key file exception"""


class MissingSecretsFile(Exception):
    """Missing secrets key file exception"""


class ConfigLoader:
    """
    Config loader class
    """

    def __init__(
        self,
        env,
        key_file_path,
        secrets_file_path,
        project_file_path,
        key_env_var_name="DJANGO_MASTER_KEY",
    ):

        self.key_file_path = key_file_path
        self.secrets_file_path = secrets_file_path
        self.project_file_path = project_file_path
        self.env = env

        try:
            with open(project_file_path, encoding="utf-8") as project_file:
                project_file_content = project_file.read()
                try:
                    self.project_data = json.loads(project_file_content)
                except JSONDecodeError as json_decode_error:
                    raise ValueError("Could not load project data") from json_decode_error
        except FileNotFoundError as file_not_found_error:
            raise MissingProjectFile from file_not_found_error

        key = os.environ.get(key_env_var_name, None)

        if key is None:
            try:
                with open(key_file_path, "rb") as key_file:
                    key = key_file.read()
            except FileNotFoundError as file_not_found_error:
                raise MissingMasterKey from file_not_found_error

        fernet = Fernet(key)

        try:
            with open(secrets_file_path, "rb") as file:
                encrypted_data = file.read()
        except FileNotFoundError as file_not_found_error:
            raise MissingSecretsFile from file_not_found_error

        decrypted = fernet.decrypt(encrypted_data)
        try:
            self.secrets_data = json.loads(decrypted)
        except JSONDecodeError as json_decode_error:
            raise ValueError("Could not load secrets data") from json_decode_error

    def get_setting(self, data, setting_name, default):
        """
        Get setting from the data dictionary. Looks first in the `environements`
        sub-dictionary, then in `common`, then finally falls back to the default value.
        """
        try:
            return data["environments"][self.env][setting_name]
        except KeyError:
            pass
        try:
            return data["common"][setting_name]
        except KeyError:
            pass

        return default

    def get_project_setting(self, setting_name, default=None):
        """
        Get setting from the project data
        """
        return self.get_setting(self.project_data, setting_name, default)

    def get_secret_setting(self, setting_name, default=None):
        """
        Get setting from the secrets data
        """
        return self.get_setting(self.secrets_data, setting_name, default)
