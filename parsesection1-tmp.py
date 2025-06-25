import xml.etree.ElementTree as ET
import pandas as pd

def extract_episode_elements(xml_file, output_csv="episode_elements.csv"):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    rows = []

    for patient in root.findall("patient"):
        patient_id = patient.attrib.get("ncdrPatientId", "")

        for episode in patient.findall("episode"):
            episode_key = episode.attrib.get("episodeKey", "")

            # Find all descendant <element> tags under the episode
            for elem in episode.findall(".//element"):
                display_name = elem.attrib.get("displayName", "")
                value_elem = elem.find("value")
                value = value_elem.attrib.get("value", "") if value_elem is not None else ""

                rows.append({
                    "Section Level": 1,
                    "Patient ID": patient_id,
                    "Episode Key": episode_key,
                    "Display Name": display_name,
                    "Value": value
                })

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(f"✅ Extracted {len(rows)} episode element rows to {output_csv}")

extract_episode_elements("CPMI999999-2025Q2.xml")
