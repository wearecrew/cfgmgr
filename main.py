import click

import os

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken


@click.group()
def cli():
    pass


def get_key(path):
    try:
        with open(path) as file:
            return file.read()
    except FileNotFoundError:
        click.echo("Key file not found, please run `secrets key`")
        raise click.Abort()


def get_decrypted(decrypted_path):
    try:
        with open(decrypted_path) as file:
            return file.read()
    except FileNotFoundError:
        click.echo("Decrypted file not found, please create one")
        raise click.Abort()


def get_encyrypted(encrypted_path):
    try:
        with open(encrypted_path) as file:
            return file.read()
    except FileNotFoundError:
        click.echo("Encrypted file not found, please create one")
        raise click.Abort()


def get_fernet(key):
    try:
        return Fernet(key)
    except:
        click.echo("Encryption failed, key file is invalid")
        raise click.Abort()


def save_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name != "":
        if not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name)
            except:
                click.echo("Could not create path")
                raise click.Abort()

    try:
        with open(path, "wb") as file:
            file.write(content)
    except:
        click.echo("Could not write file (is the path valid?)")
        raise click.Abort()


@click.command()
@click.option("key_path", "--path", type=click.Path(), required=True)
def makekey(key_path):
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
    key = get_key(key_path)
    decrypted = get_decrypted(decrypted_path)
    fernet = get_fernet(key)

    try:
        encrypted = fernet.encrypt(decrypted.encode())
    except:
        click.echo("Encryption failed (check key file?)")
        raise click.Abort()

    save_file(encrypted_path, encrypted)
    os.remove(decrypted_path)


@click.command()
@click.option("key_path", "--key", type=click.Path(), required=True)
@click.option("encrypted_path", "--in", type=click.Path(), required=True)
@click.option("decrypted_path", "--out", type=click.Path(), required=True)
def decrypt(key_path, encrypted_path, decrypted_path):
    key = get_key(key_path)
    encrypted = get_encyrypted(encrypted_path)
    fernet = get_fernet(key)

    try:
        decrypted = fernet.decrypt(encrypted.encode()).decode()
    except InvalidToken:
        click.echo("Decryption failed (check key file?)")
        raise click.Abort()

    save_file(decrypted_path, decrypted.encode(encoding="UTF-8"))
    os.remove(encrypted_path)


cli.add_command(makekey)
cli.add_command(encrypt)
cli.add_command(decrypt)
