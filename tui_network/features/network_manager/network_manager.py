import dbus
import os

from dbus import DBusException

class NetworkManager:

    def __init__(self):
        self.update_info()
        self.scan()

    def update_info(self):

        self.adapters_path = []
        self.info = []

        bus     = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("net.connman.iwd", "/"), "org.freedesktop.DBus.ObjectManager")
        objects = manager.GetManagedObjects()

        for adapter_path, interface in objects.items():
            if 'net.connman.iwd.Device' in interface:
                adapter_info = {
                    'device': None,
                    'status': None
                }   
                for sub_path, sub_interface in interface.items():
                    if sub_path == 'net.connman.iwd.Device':
                        adapter_info['device'] = {
                            'Name': str(sub_interface['Name']),
                            'Address': str(sub_interface['Address']),
                            'Powered': bool(sub_interface['Powered']),
                            'Mode': str(sub_interface['Mode'])
                        }
                    if sub_path == 'net.connman.iwd.Station':
                        connected_network = str(sub_interface['ConnectedNetwork'])
                        adapter_info['status'] = {
                            'State': str(sub_interface['State']),
                            'Network': str(objects[connected_network]['net.connman.iwd.Network']['Name']),
                        }
                self.adapters_path.append(adapter_path)
                self.info.append(adapter_info)
    
    def get_devices(self):
        return [x['device'] for x in self.info]

    def get_status(self):
        return [x['status'] for x in self.info]
    
    def scan(self):
        
        device_name = self.adapters_path[0]

        bus = dbus.SystemBus()
        device = dbus.Interface(bus.get_object("net.connman.iwd", device_name), "net.connman.iwd.Station")
        try:
            device.Scan()
        except DBusException:
            print('Operation already in progress...')
    
    def get_networks(self):
        
        bus     = dbus.SystemBus()
        manager = dbus.Interface(bus.get_object("net.connman.iwd", "/"), "org.freedesktop.DBus.ObjectManager")
        objects = manager.GetManagedObjects()

        networks = []
        for _, interface in objects.items():
            if 'net.connman.iwd.Network' in interface:
                for sub_path, sub_interface in interface.items():
                    if sub_path == 'net.connman.iwd.Network':
                        networks.append(
                            {
                                'Name': str(sub_interface['Name']),
                            }
                        )
        return networks
    
    def connect(self, network_name, network_passphrase):
        command = f'iwctl --passphrase "{network_passphrase}" station {self.info[0]["device"]["Name"]} connect "{network_name}"'
        os.popen(command)

    def disconnect(self):
        device_name = self.adapters_path[0]

        bus = dbus.SystemBus()
        device = dbus.Interface(bus.get_object("net.connman.iwd", device_name), "net.connman.iwd.Station")
        device.Disconnect()

    def toggle(self, up: bool):
        device_name = self.adapters_path[0]

        bus = dbus.SystemBus()
        device = dbus.Interface(bus.get_object("net.connman.iwd", device_name), "org.freedesktop.DBus.Properties")
        if up:
            device.Set("net.connman.iwd.Device", "Powered", dbus.Boolean(1))
        else:
            device.Set("net.connman.iwd.Device", "Powered", dbus.Boolean(0))