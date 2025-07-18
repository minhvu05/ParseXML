import xml.etree.ElementTree as ET
import pandas as pd

## MAYBE INCORRECT DOUBLE CHECK

# only looking at the admin section of xml file
def parse_admin(file):
    # initializing etree, data, and naming vars 
    tree = ET.parse(file)
    root = tree.getroot()
    data = []
    base_name = file.split('.')[0]
    transmission_number = ""

    # focusing on admin section only
    admin_section = root.find(".//submission/section[@code='ADMIN']")

    # looping through all elements under admin section
    for elem in admin_section.findall("element"):
        display_name = elem.attrib.get("displayName", "")
        value_element = elem.find("value")

        # checking if there is actually a value associated w/ display
        if value_element is not None:
            value = value_element.attrib.get("value", "") 
        else:
            value = ""

        # keeping the transmission number
        if display_name == "Transmission Number":
            transmission_number = value

        data.append((display_name, value))

    # putting into csv
    df = pd.DataFrame(data, columns = ["display_name", "value"])
    output_name = f"{base_name}-{transmission_number}.csv"
    df.to_csv(output_name, index = False)



print(parse_admin("CPMI999999-2025Q2.xml"))
