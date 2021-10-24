"""
This module provides the command line interface functions to make keys,
encrypt files and decrypt files
"""

import os

import click
from cryptography.fernet import Fernet, InvalidToken


def get_key(path):
    """
    Open the specified key file path and read the data,
    echo an error if the file is missing
    """
    try:
        with open(path, "rb") as file:
            return file.read()
    except FileNotFoundError as file_not_found:
        click.echo("Key file not found, please run `cfgmgr makekey`")
        raise click.Abort() from file_not_found


def get_decrypted(path):
    """
    Open the specified decrypted file path and read the data,
    echo an error if the file is missing
    """
    try:
        with open(path, "rb") as file:
            return file.read()
    except FileNotFoundError as file_not_found:
        click.echo("Decrypted file not found, please create one")
        raise click.Abort() from file_not_found


def get_encyrypted(path):
    """
    Open the specified encrypted file path and read the data,
    echo an error if the file is missing
    """
    try:
        with open(path, "rb") as file:
            return file.read()
    except FileNotFoundError as file_not_found:
        click.echo("Encrypted file not found, please create one")
        raise click.Abort() from file_not_found


def get_fernet(key):
    """
    Take a key and return a Fernet object,
    echo an error if the key is invalid
    """
    try:
        return Fernet(key)
    except Exception as invalid_key:
        click.echo("Encryption failed, key file is invalid")
        raise click.Abort() from invalid_key


def save_file(path, content):
    """
    Save content to path, echo an error if path is not valid
    """
    dir_name = os.path.dirname(path)
    if dir_name != "":
        if not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name)
            except Exception as invalid_path:
                click.echo("Could not create path")
                raise click.Abort() from invalid_path

    try:
        with open(path, "wb") as file:
            file.write(content)
    except Exception as invalid_path:
        click.echo("Could not write file (is the path valid?)")
        raise click.Abort() from invalid_path


@click.command()
@click.option("key_path", "--path", type=click.Path(), required=True)
def makekey(key_path):
    """
    Create a Fernet key and save to the supplied path
    """
    key = Fernet.generate_key()
    if os.path.isfile(key_path):
        click.echo("Master key already exists!")
        raise click.Abort()
    save_file(key_path, key)


@click.command()
@click.option("key_path", "--key", type=click.Path(), required=True)
@click.option("decrypted_path", "--in", type=click.Path(), required=True)
@click.option("encrypted_path", "--out", type=click.Path(), required=True)
def encrypt(key_path, decrypted_path, encrypted_path):
    """
    Read the content from the decrypted file path,
    write the encrypted content back to the encrypted file path,
    then delete the original decrypted file
    """
    key = get_key(key_path)
    decrypted = get_decrypted(decrypted_path)
    fernet = get_fernet(key)

    try:
        encrypted = fernet.encrypt(decrypted)
    except Exception as encryption_failed:
        click.echo("Encryption failed (check key file?)")
        raise click.Abort() from encryption_failed

    save_file(encrypted_path, encrypted)
    os.remove(decrypted_path)


@click.command()
@click.option("key_path", "--key", type=click.Path(), required=True)
@click.option("encrypted_path", "--in", type=click.Path(), required=True)
@click.option("decrypted_path", "--out", type=click.Path(), required=True)
def decrypt(key_path, encrypted_path, decrypted_path):
    """
    Read the content from the encrypted file path,
    write the decrypted content back to the decrypted file path,
    then delete the original encrypted file
    """
    key = get_key(key_path)
    encrypted = get_encyrypted(encrypted_path)
    fernet = get_fernet(key)

    try:
        decrypted = fernet.decrypt(encrypted)
    except InvalidToken as decryption_failed:
        click.echo("Decryption failed (check key file?)")
        raise click.Abort() from decryption_failed

    save_file(decrypted_path, decrypted)
    os.remove(encrypted_path)


@click.group()
def cli():
    """
    Click CLI for cfgmgr
    """


cli.add_command(makekey)
cli.add_command(encrypt)
cli.add_command(decrypt)
