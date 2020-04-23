"""
Main library
"""
import requests
import requirements

from subprocess import call

from readsettings import ReadSettings
data = ReadSettings("pio.json")


def getVersionList(package):
    return list(
        requests.get("https://pypi.org/pypi/{}/json".format(package)).json()
        ["releases"].keys())


def add(args):
    for i in enumerate(args):
        latest = getVersionList(i[1])[-1]

        call(["pip", "install", "{}~={}".format(i[1], latest)])

        data[i[1]] = latest


def remove(args):
    for i in enumerate(args):
        call(["pip", "uninstall", i[1]])
        del data[i[1]]


def install(args):
    for key in data.json().keys():
        pair = (key, data.json()[key])
        call(["pip", "install", "{}~={}".format(pair[0], pair[1])])


def upgrade(args=False):
    if not args:
        args = data.json().keys()

    for i in enumerate(args):
        latest = getVersionList(i[1])[-1]

        call(["pip", "install", "--upgrade", "{}~={}".format(i[1], latest)])

        data[i[1]] = latest


def migrate(args):
    with open(args[0], "r") as f:
        for req in requirements.parse(f):
            data[req.name] = req.specs[0][1]
