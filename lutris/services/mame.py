"""MAME service
Not ready yet"""
from gettext import gettext as _

from lutris.services.base import BaseService


class MAMEService(BaseService):
    """Service class for MAME"""
    type = "mame"
    name = _("MAME")
    icon = "mame"
