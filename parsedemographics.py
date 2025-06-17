import xml.etree.ElementTree as ET
import pandas as pd

def parse_demographics(file):
    tree = ET.parse(file)
    root = tree.getroot()
    data = []
    base_name = file.split('.')[0]
    transmission_number = ""

    # focusing on admin section only
    admin_section = root.find(".//submission/section[@code='ADMIN']")

    # looping through all elements under admin section
    # can probably do this easier w OOP implementation
    for elem in admin_section.findall("element"):
        display_name = elem.attrib.get("displayName", "")
        value_element = elem.find("value")
        if value_element is not None:
            value = value_element.attrib.get("value", "") 
        else:
            value = ""
        if display_name == "Transmission Number":
            transmission_number = value
        
    
    
    for patient in root.findall("patient"):
        # get patient id
        patient_id = patient.attrib.get("ncdrPatientId", "")

        # create only these cols for patients
        info = {
            "ncdrPatientId": patient_id,
            "Last Name": "",
            "First Name": "",
            "SSN": "",
            "Birth Date": "",
            "Sex": "",
            "Patient Zip Code": ""
        }
        # arr -> dict

        # looking inside demographics section only
        demo_section = patient.find("section[@code='DEMOGRAPHICS']")
        for elem in demo_section.findall("element"):
            display_name = elem.attrib.get("displayName", "")
            value_elem = elem.find("value")

            if value_elem is not None: 
                value = value_elem.attrib.get("value", "") 
            else:
                value = ""

            # if the display falls under one of the cols
            if display_name in info:
                info[display_name] = value

        data.append(info)


    # putting into csv
    df = pd.DataFrame(data)
    output_name = f"{base_name}-{transmission_number}-demographics.csv"
    df.to_csv(output_name, index=False)

parse_demographics("CPMI999999-2025Q2.xml")