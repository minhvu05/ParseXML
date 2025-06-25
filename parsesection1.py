# proof of concept
import xml.etree.ElementTree as ET
import pandas as pd

def extract_episode_data(xml_path: str, csv_path: str):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    rows = []
    global_counter = 1

    for patient in root.findall('patient'):
        ncdr_id = patient.get('ncdrPatientId')
        for episode in patient.findall('episode'):
            episode_key = episode.get('episodeKey')
            rows.append({
                'ncdrPatientId': ncdr_id,
                'episodeKey': episode_key,
                'episodeIndex': global_counter
            })
            global_counter += 1

    df = pd.DataFrame(rows)
    output_name = f"episode_file1.csv"
    df.to_csv(output_name, index=False)


# def extract_episode_head_sections(xml_path: str, index_csv_path: str, output_csv_path: str):
#     # Load the episode index (from previous method)
#     index_df = pd.read_csv(index_csv_path)
#     index_lookup = {
#         (str(row['ncdrPatientId']), str(row['episodeKey'])): row['episodeIndex']
#         for _, row in index_df.iterrows()
#     }

#     tree = ET.parse(xml_path)
#     root = tree.getroot()

#     rows = []

#     for patient in root.findall('patient'):
#         ncdr_id = patient.get('ncdrPatientId')
#         for episode in patient.findall('episode'):
#             episode_key = episode.get('episodeKey')
#             index = index_lookup.get((ncdr_id, episode_key))
#             if index is None:
#                 continue

#             for section in episode.findall('section'):
#                 code = section.attrib.get('code')
#                 display = section.attrib.get('displayName')
#                 if code and display:
#                     rows.append({
#                         'episodeIndex': index,
#                         'ncdrPatientId': ncdr_id,
#                         'episodeKey': episode_key,
#                         'code': code,
#                         'displayName': display
#                     })

    df = pd.DataFrame(rows)
    output_name = f"episode_file2.csv"
    df.to_csv(output_name, index=False)

print(extract_episode_data('CPMI999999-2025Q2.xml', 'episode_data.csv'))
#print(extract_episode_head_sections('CPMI999999-2025Q2.xml', extract_episode_data('CPMI999999-2025Q2.xml', 'episode_data.csv'), 'episode_data.csv'))