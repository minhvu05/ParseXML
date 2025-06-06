import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("CPMI999999-2025Q2.xml")
root = tree.getroot()

# only looking at admin section of xml file
admin_section = root.find(".//submission/section[@code='ADMIN']")

# if admin section in file
if admin_section is not None:
    # looping through all elements
    for e in admin_section.findall("element"):
        display_name = e.attrib.get("displayName", "")
        value_element = e.find("value")
        # checking if there is actually a value associated w/ display
        value = value_element.attrib.get("value", "") if value_element is not None else ""
        print(f"{display_name}: {value}")
else:
    print("ADMIN section not found.")


