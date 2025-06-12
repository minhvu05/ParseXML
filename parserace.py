import xml.etree.ElementTree as ET
import pandas as pd

def parse_race(file):
    tree = ET.parse(file)
    root = tree.getroot()
    data = []
    base_name = file.split('.')[0]

    # creating cols
    race_labels = {
        "White", 
        "Black/African American", 
        "Asian", 
        "American Indian/Alaskan Native", 
        "Native Hawaiian/Pacific Islander"
    }

    # looping through all elements under patient section
    for patient in root.findall("patient"):
        patient_id = patient.attrib.get("ncdrPatientId", "")

        # looking at only demographics
        demo_section = patient.find("section[@code='DEMOGRAPHICS']")
        for elem in demo_section.findall("element"):
            display_name = elem.attrib.get("displayName", "")
            value_elem = elem.find("value")
            if value_elem is not None:
                value = value_elem.attrib.get("value", "") 
            else:
                value = ""

            # check if it falls under the race categories and is true
            if display_name in race_labels and value.lower() == "true":
                data.append({
                    "ncdrPatientId": patient_id,
                    "Race": display_name
                })


    # putting into csv
    df = pd.DataFrame(data)
    output_name = f"{base_name}-race.csv"
    df.to_csv(output_name, index=False)

parse_race("CPMI999999-2025Q2.xml")
