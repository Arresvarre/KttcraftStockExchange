
from mcuuid import MCUUID
import requests
import json

def valid_mc_name(mc_name):
    return True



def valid_uuid(uuid):
    return True


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
