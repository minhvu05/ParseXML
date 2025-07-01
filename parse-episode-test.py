import xml.etree.ElementTree as ET
import pandas as pd

class Processor():
    def __init__(self, file):
        self.file = file
        self.counter = 1  # initialize the counter
        self.section_counter = 1 # initialize the second counter

    def get_episode(self):

        tree = ET.parse(self.file)
        root = tree.getroot()

        data = []
        self.counter = 1  # reset for fresh runs

        for patient in root.findall('.//patient'):
            patientid = patient.attrib.get('ncdrPatientId')
            for episode in patient.findall('episode'):
                episodekey = episode.attrib.get('episodeKey')
                data.append((patientid, episodekey, self.counter))
                self.counter += 1

        df = pd.DataFrame(data, columns=["patientid", "episodekey", "counter"])
        output_name = "episode.csv"
        df.to_csv(output_name, index = False)

    def get_section1(self):
        tree = ET.parse(self.file)
        root = tree.getroot()

        data = []
        self.section_counter = 1  # reset

        for patient in root.findall('.//patient'):
            patientid = patient.attrib.get('ncdrPatientId')
            for episode in patient.findall('episode'):
                episodekey = episode.attrib.get('episodeKey')
                # Only the direct <section> children of <episode> (level 1)
                for section in episode.findall('section'):
                    display_name = section.attrib.get('displayName')
                    code = section.attrib.get('code')
                    data.append((
                        self.section_counter,
                        patientid,
                        episodekey,
                        display_name,
                        code
                    ))
                    self.section_counter += 1

        df = pd.DataFrame(data, columns=["section_level1_key", "patientid", "episodekey", "displayName", "code"])
        output_name = "section-level1.csv"
        df.to_csv(output_name, index = False)



p = Processor("CPMI999999-2025Q2.xml")
p.get_episode()
p.get_section1()
