import os
import xml.etree.ElementTree as ET
import argparse
import manage_data
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--dept", help="french departement number to process")
parser.add_argument("--gas-type", help="king of fuel to process")

args = parser.parse_args()


class Pomp(object):
    def __init__(self, node) -> None:
        super().__init__()
        self.node = node
        self.tag_list = [item.tag for item in node]
        self.attrib_list = [item.attrib for item in node]
        self.text_list = [item.text for item in node]
        self.latitude = node.attrib["latitude"]
        self.longitude = node.attrib["longitude"]
        self.adress = node[0].text
        self.city = node[1].text
        self.cp = node.attrib["cp"]
        self.id = node.attrib["id"]
        # self.others = [node[][i].text for i in range(len(node[2]))]

    def info(self):
        string = ""
        for key, value, data, index in zip(
            self.tag_list, self.text_list, self.attrib_list, range(len(self.tag_list))
        ):
            if key == "services":
                string += f"""{key} : {', '.join([self.node[index][i].text for i in range(len(self.node[index]))])}\n"""
            elif key == "prix":
                keys = list(data.keys())
                keys.remove("id")
                string += f"""{key} : {data['nom']} : {data['valeur']} € (dernière mise à jour {data['maj']})\n"""
            elif data == {}:
                string += f"""{key} : {value}\n"""
            else:
                string += f"""{key} : {value}
                                    {data}\n"""
        return string


tree = ET.parse("../../data/PrixCarburants_instantane.xml")
root = tree.getroot()
interesting_pomp = [
    Pomp(item).info() for item in root if item.attrib["cp"][:2] == args.dept
]
print(interesting_pomp[19])
