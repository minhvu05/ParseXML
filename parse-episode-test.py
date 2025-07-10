import xml.etree.ElementTree as ET
import pandas as pd

class Processor():
    def __init__(self, file):
        self.file = file
        self.episode_counter = 1
        self.episode_dict = {}  # key: episodeKey / value: episode_counter
        self.section_counters = {}  # key: level / level: counter (per section)
        self.section_data = {}      # key: level / level: row data

    def get_episode(self):
        tree = ET.parse(self.file)
        root = tree.getroot()
        data = []
        self.episode_counter = 1 # reset count & dict
        self.episode_dict = {} 

        for patient in root.findall('.//patient'):
            patientid = patient.attrib.get('ncdrPatientId')
            for episode in patient.findall('episode'):
                episodekey = episode.attrib.get('episodeKey')
                self.episode_dict[episodekey] = self.episode_counter 
                data.append((patientid, episodekey, self.episode_counter))
                self.episode_counter += 1

        df = pd.DataFrame(data, columns=["patientId", "episodeKey", "episodeCounter"])
        df.to_csv("episode.csv", index = False)

    def process_section(self, section, level, parent_counter, patientid, episodekey, episode_counter):
        if level not in self.section_counters:
            self.section_counters[level] = 1
            self.section_data[level] = []

        current_counter = self.section_counters[level]
        display_name = section.attrib.get("displayName")
        code = section.attrib.get("code")

        self.section_data[level].append((
            current_counter,
            parent_counter,
            episode_counter,
            patientid,
            episodekey,
            display_name,
            code
        ))

        self.section_counters[level] += 1

        for child_section in section.findall("section"):
            self.process_section(
                child_section, 
                level + 1, 
                current_counter, 
                patientid, 
                episodekey,
                episode_counter  
            )


    def extract_sections_by_level(self):
        tree = ET.parse(self.file)
        root = tree.getroot()
        self.section_counters = {}
        self.section_data = {}

        for patient in root.findall('.//patient'):
            patientid = patient.attrib.get('ncdrPatientId')
            for episode in patient.findall('episode'):
                episodekey = episode.attrib.get('episodeKey')

                episode_counter = self.episode_dict.get(episodekey)

                for section in episode.findall('section'):
                    self.process_section(
                        section=section,
                        level=1,
                        parent_counter=None,
                        patientid=patientid,
                        episodekey=episodekey,
                        episode_counter=episode_counter  # pass down
                    )

        for level, rows in self.section_data.items():
            df = pd.DataFrame(rows, columns=[
                f"section{level}_counter",
                f"section{level-1}_counter" if level > 1 else "parent",
                "episode_counter",
                "patientid",
                "episodekey",
                "displayName",
                "code"
            ])
            output_name = f"section-level{level}.csv"
            df.to_csv(output_name, index = False)



p = Processor("CPMI999999-2025Q2.xml")
p.get_episode()
p.extract_sections_by_level()
