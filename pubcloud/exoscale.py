import json as JS
import xml.etree.ElementTree as ET
import os.path
import pickle

EXOSCALE_FILE = '/etc/exoscale_regionSMT.json'

if os.path.exists(EXOSCALE_FILE):
    with open(EXOSCALE_FILE, "rb") as dict_file:
        data = JS.loads(dict_file.read())
        print(str(data))
        root = ET.Element("regionSMTdata")
        smtinfo = ET.SubElement(root, "smtInfo")
        
        for key, val in data.items():
            child = ET.Element(key)
            #print(key, val)
            child.text = str(val)
            smtinfo.append(child)
    
    print(ET.tostring(root, encoding='utf8', method='xml'))