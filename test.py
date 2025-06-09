import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("CPMI999999-2025Q2.xml")
root = tree.getroot()

patients = []

race_labels = {
    "White", 
    "Black/African American", 
    "Asian", 
    "American Indian/Alaskan Native", 
    "Native Hawaiian/Pacific Islander"
}

for patient in root.findall("patient"):
    patient_id = patient.attrib.get("ncdrPatientId", "")
    selected_races = []

    demo_section = patient.find("section[@code='DEMOGRAPHICS']")
    if demo_section is not None:
        for elem in demo_section.findall("element"):
            label = elem.attrib.get("displayName", "")
            value_elem = elem.find("value")
            value = value_elem.attrib.get("value", "") if value_elem is not None else ""

            # Check if it's a race and selected
            if label in race_labels and value.lower() == "true":
                selected_races.append(label)

    # Only add if at least one race is selected
    if selected_races:
        patients.append({
            "ncdrPatientId": patient_id,
            "Race(s)": ", ".join(selected_races)
        })

print(patients) 
