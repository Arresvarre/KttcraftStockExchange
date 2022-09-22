
from mcuuid import MCUUID
from mcuuid.tools import is_valid_minecraft_username, is_valid_mojang_uuid
import requests
import json

def valid_mc_name(mc_name):
    return is_valid_minecraft_username(mc_name)


def valid_uuid(uuid):
    return is_valid_mojang_uuid(uuid)


def mc_name_to_UUID(name):
    player = MCUUID(name=name)
    return player.uuid


def mc_name_to_UUID(name):
    r = requests.get("https://api.mojang.com/user/profile/minecraft/{name}".format(
        name=name,
    ), headers={
        'Content-Type': 'application/json',
    })
    result = r.content

    return json.loads(result)["id"]


def UUID_to_mc_name(uuid):
    r = requests.get("https://api.mojang.com/user/profile/{uuid}".format(
        uuid=uuid,
    ), headers={
        'Content-Type': 'application/json',
    })
    result = r.content

    return json.loads(result)["name"]


def mc_head(uuid):
    return 'https://crafatar.com/avatars/' + uuid