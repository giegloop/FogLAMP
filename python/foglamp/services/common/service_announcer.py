# -*- coding: utf-8 -*-

# FOGLAMP_BEGIN
# See: http://foglamp.readthedocs.io/
# FOGLAMP_END

"""Common FoglampMicroservice Class"""

import foglamp.services.common.avahi as avahi
from foglamp.common import logger
import dbus
import socket

__author__ = "Mark Riddoch, Amarendra K Sinha"
__copyright__ = "Copyright (c) 2017 OSIsoft, LLC"
__license__ = "Apache 2.0"
__version__ = "${VERSION}"

_LOGGER = logger.setup(__name__)


class ServiceAnnouncer:
    _service_name = None
    """ The name of the service to advertise """

    _group = None
    """ The Avahi group """

    def __init__(self, name, service, port, txt=None):
        try:
            bus = dbus.SystemBus()
            server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER), avahi.DBUS_INTERFACE_SERVER)
            self._group = dbus.Interface(bus.get_object(avahi.DBUS_NAME, server.EntryGroupNew()),
                                     avahi.DBUS_INTERFACE_ENTRY_GROUP)

            host = self.get_ip()
            self._service_name = "{}-{}".format(name, host.split(".")[3])
            index = 1
            txt_new = ['FogLAMP Service' if txt is None else txt, host]
            while True:
                try:
                    self._group.AddService(avahi.IF_UNSPEC, avahi.PROTO_INET, 0, self._service_name, service, '', '', port,
                                       avahi.string_array_to_txt_array(txt_new))
                except dbus.DBusException:  # name collision -> rename
                    index += 1
                    self._service_name = '%s #%s' % (name, str(index))
                else:
                    break

            self._group.Commit()
        except Exception:
            _LOGGER.error("Avahi not available, continuing without service discovery available")

    @property
    def get_service_name(self):
        return self._service_name

    def unregister(self):
        if self._group is not None:
            self._group.Reset()
            self._group = None

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
