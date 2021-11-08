
from mcuuid import MCUUID
from mcuuid.tools import is_valid_minecraft_username, is_valid_mojang_uuid

def valid_mc_name(mc_name):
    return is_valid_minecraft_username(mc_name)


def valid_uuid(uuid):
    return is_valid_mojang_uuid(uuid)


def mc_name_to_UUID(name):
    player = MCUUID(name=name)
    return player.uuid


def UUID_to_mc_name(uuid):
    player = MCUUID(uuid=uuid)
    return player.name


def mc_head(uuid):
    return 'https://crafatar.com/avatars/' + uuid