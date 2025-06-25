# OOP Implentation of parse admin, demographic, race, and ethnicity
import xml.etree.ElementTree as ET
import pandas as pd

class Parser():
    # constructor
    def __init__(self, file):
        self.file = file
        self.base_name = self.file.split('.')[0]

    # tree getter method
    def get_tree(self):
        tree = ET.parse(self.file)
        return tree
    
    # root getter method
    def get_root(self):
        root = self.get_tree().getroot()
        return root
    
    # returns the file's base name
    def get_base(self):
        return self.file.split('.')[0]
    
    def get_value(self, value_elem):
        if value_elem is not None: 
                return value_elem.attrib.get("value", "") 
        else:
            return ""

    # storing the transmission number
    def get_transmission(self):
        # looking only through the admin section
        root = self.get_root()
        admin_section = root.find(".//submission/section[@code='ADMIN']")

        for elem in admin_section.findall("element"):
            display_name = elem.attrib.get("displayName", "")
            value_element = elem.find("value")

            # extract the value from each element
            if value_element is not None:
                value = value_element.attrib.get("value", "") 
            else:
                value = ""

            # returns the value associated w transmission if found
            if display_name == "Transmission Number":
                return value

        # if not found, return 0
        return 0

    # to_csv for parsing admin section only
    def to_csv(self, arr, output_name) :
        df = pd.DataFrame(arr)
        df.to_csv(output_name, index = False)

    # parses the admin section 
    #todo for element -> value where there are 2 display names, what do we do w 2nd one?
    def parse_admin(self):
        root = self.get_root()
        data = []
        admin_section = root.find(".//submission/section[@code='ADMIN']")

        for elem in admin_section.findall("element"):
            display_name = elem.attrib.get("displayName", "")
            value_elem = elem.find("value")
            code = elem.attrib.get("code", "")
            codeSystem = elem.attrib.get("codeSystem", "")

            # checking if there is actually a value associated w/ display
            value = self.get_value(value_elem)

            data.append({
                "Display Name": display_name,
                "Value": value,
                "Code": code,
                "CodeSystem": codeSystem
            })
        
        # not using overriden .to_csv() method bc param differences (? maybe could fix ?)
        df = pd.DataFrame(data)
        output_name = f"{self.get_base()}-{self.get_transmission()}.csv"
        df.to_csv(output_name, index = False)

    # parses the demographic section
    def parse_demographics(self):
        root = self.get_root()
        data = []
        
        for patient in root.findall("patient"):
            # get patient id
            patient_id = patient.attrib.get("ncdrPatientId", "")

            # defining new info dict for each patient
            info = {
                "ncdrPatientId": patient_id,
                "Last Name": "",
                "First Name": "",
                "SSN": "",
                "Birth Date": "",
                "Sex": "",
                "Patient Zip Code": ""
            }

            # looking inside demographics section only
            demo_section = patient.find("section[@code='DEMOGRAPHICS']")
            for elem in demo_section.findall("element"):
                display_name = elem.attrib.get("displayName", "")
                value_elem = elem.find("value")

                value = self.get_value(value_elem)

                # if the display falls under one of the cols
                if display_name in info:
                    info[display_name] = value

            data.append(info)


        # putting into csv
        df = pd.DataFrame(data)
        output_name = f"{self.get_base()}-{self.get_transmission()}-demographics.csv"
        df.to_csv(output_name, index=False)
    
    # parses the races
    def parse_race(self):
        root = self.get_root()
        data = []

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

            # looking at only in demographics section
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
        output_name = f"{self.get_base()}-race.csv"
        df.to_csv(output_name, index=False)
    
    # parses the ethnicities
    def parse_ethnicity(self):
        root = self.get_root()
        ethnicity_rows = []

        # only value we're looking for
        ethnicity = "Hispanic or Latino Ethnicity"

        for patient in root.findall("patient"):
            patient_id = patient.attrib.get("ncdrPatientId", "")

            # again, only looking in demo section for ethnicities
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
        output_name = f"{self.get_base()}-ethnicity.csv"
        df.to_csv(output_name, index=False)

    def episode_placeholder_name(self):
        return 0


parser = Parser("CPMI999999-2025Q2.xml")
parser.parse_admin()
parser.parse_demographics()
parser.parse_race()
parser.parse_ethnicity()


