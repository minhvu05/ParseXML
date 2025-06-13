import xml.etree.ElementTree as ET
import pandas as pd

def parse_ethnicity(file):
    tree = ET.parse(file)
    root = tree.getroot()
    ethnicity_rows = []
    base_name = file.split('.')[0]

    # only value we're looking for
    ethnicity = "Hispanic or Latino Ethnicity"

    for patient in root.findall("patient"):
        patient_id = patient.attrib.get("ncdrPatientId", "")

        demo_section = patient.find("section[@code='DEMOGRAPHICS']")
        if demo_section is not None:
            for elem in demo_section.findall("element"):
                label = elem.attrib.get("displayName", "")
                value_elem = elem.find("value")
                if value_elem is not None:
                    value = value_elem.attrib.get("value", "") 
                else:
                    value = ""

                # if the value is the target ethnicity and true
                if label == ethnicity and value.lower() == "true":
                    ethnicity_rows.append({
                        "ncdrPatientId": patient_id,
                        "Ethnicity": "Hispanic or Latino"
                    })

    df = pd.DataFrame(ethnicity_rows)
    output_name = f"{base_name}-ethnicity.csv"
    df.to_csv(output_name, index=False)

parse_ethnicity("CPMI999999-2025Q2.xml")