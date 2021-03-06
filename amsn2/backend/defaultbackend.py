""" Backend used to save the config on the home directory of the user """

import os
"""ElementTree independent from the available distribution"""
try:
    from xml.etree.cElementTree import *
except ImportError:
    try:
        from cElementTree import *
    except ImportError:
        from elementtree.ElementTree import *
from amsn2.core.config import aMSNConfig

def getPassword(passwdElmt):
    return passwdElmt.text

def setPassword(password, root_section):
    elmt = SubElement(root_section, "password", backend='DefaultBackend')
    elmt.text = password
    return elmt


def saveConfig(account, config):
    #TODO: improve
    root_section = Element("aMSNConfig")
    for e in config._config:
        val = config._config[e]
        elmt = SubElement(root_section, "entry",
                          type=type(val).__name__,
                          name=str(e))
        elmt.text = str(val)

    accpath = os.path.join(account.account_dir, "config.xml")
    xml_tree = ElementTree(root_section)
    xml_tree.write(accpath, encoding='utf-8')

def loadConfig(account):
    c = aMSNConfig()
    c.setKey("ns_server", "messenger.hotmail.com")
    c.setKey("ns_port", 1863)
    configpath = os.path.join(account.account_dir, "config.xml")
    try:
        configfile = file(configpath, "r")
    except IOError:
        return c
    configfile = file(configpath, "r")
    root_tree = ElementTree(file=configfile)
    configfile.close()
    config = root_tree.getroot()
    if config.tag == "aMSNConfig":
        lst = config.findall("entry")
        for elmt in lst:
            if elmt.attrib['type'] == 'int':
                c.setKey(elmt.attrib['name'], int(elmt.text))
            else:
                c.setKey(elmt.attrib['name'], elmt.text)
    return c
