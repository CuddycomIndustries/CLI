import os
import secrets
import requests
import json
import codecs
from pathlib import Path

from factioncli.processing.cli import log
from factioncli.processing.cli.printing import print_output

config_file_path = '/opt/faction/global/config.json'

def get_config():
    log.debug("Loading Config..")
    config = dict()
    if os.path.exists(config_file_path):
        with open(config_file_path) as f:
            config = json.load(f)
    return config

def write_config(config):
    print_output("Writing Faction config file..")
    config_dir = os.path.dirname(config_file_path)
    path = Path(config_dir)
    path.mkdir(parents=True, exist_ok=True)
    with open(config_file_path, 'wb+') as f:
        json.dump(config, codecs.getwriter('utf-8')(f), ensure_ascii=False, indent=2, sort_keys=True)

def generate_config_file(admin_username,
                         admin_password,
                         api_upload_dir,
                         build,
                         console_port,
                         containers,
                         docker_network_name,
                         external_address,
                         faction_path,
                         flask_secret,
                         postgres_host,
                         postgres_database,
                         postgres_username,
                         postgres_password,
                         rabbit_host,
                         rabbit_username,
                         rabbit_password,
                         system_username,
                         system_password,
                         ):

    if not flask_secret:
        flask_secret = secrets.token_urlsafe(64)

    if not admin_password:
        admin_password = secrets.token_urlsafe(16)

    if not system_password:
        system_password = secrets.token_urlsafe(64)

    if not postgres_password:
        postgres_password = secrets.token_urlsafe(64)

    if not rabbit_password:
        rabbit_password = secrets.token_urlsafe(64)

    if not external_address:
        external_address = "https://{0}".format(requests.get("https://api.ipify.org").text)

    containers_list = []
    for container in containers:
        containers_list.append(container)

    config = dict({
        "ADMIN_USERNAME": admin_username,
        "ADMIN_PASSWORD": admin_password,
        "API_UPLOAD_DIR": api_upload_dir,
        "BUILD": build,
        "CONSOLE_PORT": console_port,
        "CONTAINERS": containers_list,
        "EXTERNAL_ADDRESS": external_address,
        "DOCKER_NETWORK_NAME": docker_network_name,
        "FACTION_PATH": faction_path,
        "FLASK_SECRET": flask_secret,
        "RABBIT_HOST": rabbit_host,
        "RABBIT_USERNAME": rabbit_username,
        "RABBIT_PASSWORD": rabbit_password,
        "SYSTEM_USERNAME": system_username,
        "SYSTEM_PASSWORD": system_password,
        "POSTGRES_HOST": postgres_host,
        "POSTGRES_DATABASE": postgres_database,
        "POSTGRES_USERNAME": postgres_username,
        "POSTGRES_PASSWORD": postgres_password
    })

    write_config(config)