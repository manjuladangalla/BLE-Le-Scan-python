#!/usr/bin/python
#
# March 2015
# Function to scan for Bluetooth devices in python using pydbus library (which
# depends on PyGI)
#
#
# Code by Mandar Harshe @ LORIA, Nancy, France
# (mandar.harshe@inria.fr)

from __future__ import absolute_import, print_function, unicode_literals

from pydbus import SystemBus
from xml.etree import ElementTree as ET

from gi.repository import GObject
import time
import os

SERVICE_NAME = 'org.bluez'
FILE_NAME = 'ledevice.txt'
SUFFIX = '.tmp'
def find_adapter(sysbus):
    '''Find the hci device to which controls bluetooth

    '''
    tmpbluez = sysbus.get(SERVICE_NAME)
    xmltree = ET.fromstring(tmpbluez.Introspect()[0])
    adapter_list = xmltree.findall('node')
    if len(adapter_list)==0:
        raise Exception("No Bluetooth Adapter found")
    adapter_object_path = "/" + SERVICE_NAME.replace(".","/") + "/" + adapter_list[0].attrib['name']
    adapter_bus = sysbus.get(SERVICE_NAME, adapter_object_path)
    return adapter_bus

def add_le_devices(bluez_adapter, om):
    '''Get the Bluetooth devices nearby and add them to a text file
    
    '''
    devices = {}
    tmpfile = FILE_NAME + SUFFIX
    bluez_adapter.StartDiscovery()
    time.sleep(20)
    objects = om.GetManagedObjects()[0]
    bluez_adapter.StopDiscovery()
    for path, interfaces in objects.iteritems():
        if "org.bluez.Device1" in interfaces:
            devices[path] = interfaces["org.bluez.Device1"]
    with open(tmpfile, 'w') as fp:
        for path, device in devices.iteritems():
            address = device['Address']
            fp.write(address)
    os.rename(tmpfile, FILE_NAME)
    print("Scan will be restarted after a timeout")

if __name__ == '__main__':
    bus = SystemBus()
    bluez = bus.get(SERVICE_NAME)
    bluez_adapter = find_adapter(bus)
    om = bus.get(SERVICE_NAME, '/')
    try:
        add_le_devices(bluez_adapter, om)
    except KeyboardInterrupt:
        bluez_adapter.StopDiscovery()
    mainloop = GObject.MainLoop() 
    timer = GObject.timeout_add_seconds(120, add_le_devices)
    mainloop.run()
