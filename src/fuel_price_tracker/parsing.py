import os
import xml.etree.ElementTree as ET


def parser(item):
    string = ""
    for it in item:
        string += it[0] + ":\n"
        for st in it[1]:
            string += f"{st} : {it[1][st]}\n"
    return string


if os.listdir("../../data/"):
    tree = ET.parse("../../data/PrixCarburants_instantane.xml")
    root = tree.getroot()
    interesting_pomp = [item for item in root if item.attrib["cp"][:2] == "86"]
    for item in interesting_pomp:
        print("Longitude :", item.attrib["longitude"], "\n")
        print("Latitude :", item.attrib["latitude"], "\n")
        print("Code Postal :", item.attrib["cp"], "\n")

        for sub_item in item:
            print(sub_item.tag, sub_item.attrib)
        print("\n\n")


else:
    import manage_data
