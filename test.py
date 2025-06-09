import xml.etree.ElementTree as ET

tree = ET.parse("CPMI999999-2025Q2.xml")
root = tree.getroot()

patients = []

for patient in root.findall("patient"):
    # Get the patient ID from the attribute
    patient_id = patient.attrib.get("ncdrPatientId", "")

    # Initialize dictionary for this patient
    info = {
        "ncdrPatientId": patient_id,
        "Last Name": "",
        "First Name": "",
        "SSN": "",
        "Birth Date": "",
        "Sex": "",
        "Patient Zip Code": ""
    }

    # Look inside the DEMOGRAPHICS section
    demo_section = patient.find("section[@code='DEMOGRAPHICS']")
    if demo_section is not None:
        for elem in demo_section.findall("element"):
            label = elem.attrib.get("displayName", "")
            value_elem = elem.find("value")
            if value_elem is not None: 
                value = value_elem.attrib.get("value", "") 
            else:
                value = ""

            if label in info:
                info[label] = value

    patients.append(info)

print(patients)
