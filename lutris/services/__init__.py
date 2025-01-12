"""Service package"""
import os

from lutris import settings
from lutris.services.amazon import AmazonService
from lutris.services.battlenet import BNET_ENABLED, BattleNetService
from lutris.services.dolphin import DolphinService
from lutris.services.ea_app import EAAppService
from lutris.services.egs import EpicGamesStoreService
from lutris.services.flathub import FlathubService
from lutris.services.gog import GOGService
from lutris.services.humblebundle import HumbleBundleService
from lutris.services.itchio import ItchIoService
from lutris.services.lutris import LutrisService
from lutris.services.mame import MAMEService
from lutris.services.origin import OriginService
from lutris.services.steam import SteamService
from lutris.services.steamwindows import SteamWindowsService
from lutris.services.ubisoft import UbisoftConnectService
from lutris.services.xdg import XDGService
from lutris.util import system
from lutris.util.dolphin.cache_reader import DOLPHIN_GAME_CACHE_FILE
from lutris.util.linux import LINUX_SYSTEM

DEFAULT_SERVICES = ["lutris", "gog", "egs", "origin", "ubisoft", "steam"]


def get_services():
    """Return a mapping of available service classes by their respective
       service type names"""
    _services = {
        "lutris": LutrisService,
        "gog": GOGService,
        "humblebundle": HumbleBundleService,
        "egs": EpicGamesStoreService,
        "itchio": ItchIoService,
        "origin": OriginService,
        "ubisoft": UbisoftConnectService,
        "amazon": AmazonService,
        "flathub": FlathubService
    }
    if BNET_ENABLED:
        _services["battlenet"] = BattleNetService
    if not LINUX_SYSTEM.is_flatpak:
        _services["xdg"] = XDGService
    if LINUX_SYSTEM.has_steam:
        _services["steam"] = SteamService
    _services["steamwindows"] = SteamWindowsService
    if system.path_exists(DOLPHIN_GAME_CACHE_FILE):
        _services["dolphin"] = DolphinService
    return _services


SERVICES = get_services()


# Those services are not yet ready to be used
WIP_SERVICES = {
    "mame": MAMEService,
    "ea_app": EAAppService,
}

if os.environ.get("LUTRIS_ENABLE_ALL_SERVICES"):
    SERVICES.update(WIP_SERVICES)


def service_type_for_id(service_id):
    """Derive the service type name from a service ID by dropping everything
       following the first tilde character"""
    return service_id.split("~", 1)[0]


def get_service(service_id):
    """Return a new service instance object for the given service ID

    Raises `KeyError` if no matching service """
    return SERVICES[service_type_for_id(service_id)](id=service_id)


def get_enabled_services():
    #FIXME: This is a bit of a hack to allow adding multi-accounts by defining extra keys in the
    #       configuration pending rework of the account settings panel to properly accommodate
    #       this new capability
    enabled_account_options = [
        account_id
        for account_id, value in settings.sio.config.items(section="services")
        if value.lower() == "true"
    ]

    result = {}
    for account_type, account_class in SERVICES.items():
        if account_class.multi_account:
            for account_id in enabled_account_options:
                if service_type_for_id(account_id) == account_type:
                    result[account_id] = account_class(id=account_id)
        else:
            if account_type in enabled_account_options:
                result[account_type] = account_class(id=account_type)
    return result
