import xml.etree.ElementTree as ET
import pandas as pd

class Processor():
    def __init__(self, file):
        self.file = file
        self.episode_counter = 1
        self.episode_dict = {}  # key: episodeKey / value: episode_counter
        self.section_counters = {}  # key: level / level: counter (per section)
        self.section_data = {}      # key: level / level: row data
        self.section_instances = {}  # key: code / value: num of instances

    def get_episode(self):
        tree = ET.parse(self.file)
        root = tree.getroot()
        data = []
        self.episode_counter = 1 # reset count & dict
        self.episode_dict = {} 

        # looping through just episodes
        for patient in root.findall('.//patient'):
            patientid = patient.attrib.get('ncdrPatientId')
            for episode in patient.findall('episode'):
                episodekey = episode.attrib.get('episodeKey')

                # assign count to key, fill array, increment count
                self.episode_dict[episodekey] = self.episode_counter 
                data.append((patientid, episodekey, self.episode_counter))
                self.episode_counter += 1

        df = pd.DataFrame(data, columns=["patientId", "episodeKey", "episodeCounter"])
        df.to_csv("episode.csv", index = False)

    def process_section(self, section, level, parent_counter, patientid, episodekey):
        # if no level (key) in section_counter dict, initialize count to 0 and create empty list (value) for section_data
        if level not in self.section_counters:
            self.section_counters[level] = 1
            self.section_data[level] = []

        # gets/uses input data and assigns it to the level in section_data dict 
        current_counter = self.section_counters[level]
        display_name = section.attrib.get("displayName")
        code = section.attrib.get("code")

        if code:
            if code not in self.section_instances:
                self.section_instances[code] = 1
            else:
                self.section_instances[code] += 1
            section_instance = self.section_instances[code]
        else:
            section_instance = None

        self.section_data[level].append((
            current_counter,
            parent_counter,
            patientid,
            episodekey,
            display_name,
            code,
            section_instance
        ))

        self.section_counters[level] += 1

        # recursion to get into nested sections
        for child_section in section.findall("section"):
            self.process_section(
                child_section, 
                level + 1, 
                current_counter, 
                patientid, 
                episodekey,
            )

    def get_section(self):
        tree = ET.parse(self.file)
        root = tree.getroot()
        # reset dicts
        self.section_counters = {}
        self.section_data = {}

        for patient in root.findall('.//patient'):
            patientid = patient.attrib.get('ncdrPatientId')

            # first loop through epi to get key and value
            for episode in patient.findall('episode'):
                episodekey = episode.attrib.get('episodeKey')

                # loop and process each section
                for section in episode.findall('section'):
                    self.process_section(
                        section=section,
                        level=1,
                        parent_counter = None,
                        patientid = patientid,
                        episodekey = episodekey,
                    )
        
        # turn data into df put into csv
        for level, rows in self.section_data.items():
            df = pd.DataFrame(rows, columns=[
                f"section{level}_key",
                f"section{level-1}_key" if level > 1 else "parent", # not sure how to remove this col just yet
                "patientid",
                "episodekey",
                "displayName",
                "code",
                "section_instance"
            ])
            output_name = f"section-level{level}.csv"
            df.to_csv(output_name, index = False)

    def get_element(self):
        tree = ET.parse(self.file)
        root = tree.getroot()

        section1_counter = 1
        data = []

        for patient in root.findall('.//patient'):
            for episode in patient.findall('episode'):
                for section in episode.findall('section'):
                    # only getting first level sections right now
                    for elem in section:
                        # skip nested sections (for now)
                        if elem.tag == 'section':
                            continue

                        code = elem.attrib.get("code")
                        codeSystem = elem.attrib.get("codeSystem")
                        displayName = elem.attrib.get("displayName")
                        # only way to handle xsi:type
                        dataType = elem.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type") 

                        # try to get nested <value> tag if valid
                        value_elem = elem.find("value")
                        if value_elem is not None:
                            value = value_elem.text or None
                            value_code = value_elem.attrib.get("code")
                            value_codeSystem = value_elem.attrib.get("codeSystem")
                            value_displayName = value_elem.attrib.get("displayName")
                        else:
                            value = elem.text or None
                            value_code = None
                            value_codeSystem = None
                            value_displayName = None

                        # adding data
                        data.append((
                            section1_counter,
                            code,
                            codeSystem,
                            displayName,
                            dataType,
                            value,
                            value_code,
                            value_codeSystem,
                            value_displayName
                        ))

                    section1_counter += 1

        # creating df and output
        df = pd.DataFrame(data, columns=[
            "section1_counter",
            "code",
            "codeSystem",
            "displayName",
            "dataType",
            "value",
            "value_code",
            "value_codeSystem",
            "value_displayName"
        ])

        output_name = f"section1_element.csv"
        df.to_csv(output_name, index = False)



p = Processor("CPMI999999-2025Q2.xml")
p.get_episode()
p.get_section()
p.get_element()
