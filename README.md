# BLE-Le-Scan-python
A small implementation of LE scan in python using [pydbus](https://github.com/LEW21/pydbus)

## Background
This assumes you have bluez5 installed on your Linux computer (tested with v5.28). Since dbus-python hasn't been updated since 2013, and is not pythonic (as described in its Readme file) I've implemented a version of bluetooth scanning using [pydbus](https://github.com/LEW21/pydbus).

The idea was to originally to use [pygattlib](https://bitbucket.org/OscarAcena/pygattlib/) for an application, but the "Scan" function in gattlib needs admin rights/root access. This is a low-tech workaround (and a small primer to access DBus in python for bluetooth) for this problem.

## Functioning
The idea is quite simple: 
  1. Start the StartDiscovery function on the `org.bluez.Adapter1` interface for 20 seconds (or any suitable time),
  2. Populate a dictionary with a list of discovered devices
  3. Store this list of devices (with interface `org.bluez.Device1`) in text file

This solution was chosen since the [signal_subscribe()](http://lazka.github.io/pgi-docs/#Gio-2.0/classes/DBusConnection.html#Gio.DBusConnection.signal_subscribe) function was not working properly. If anyone has tips on how to make dbus signal detection work with pydbus, please let me know!
