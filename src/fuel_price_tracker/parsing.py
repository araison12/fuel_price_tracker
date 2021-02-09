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
    val = [
        [(item[i].tag, item[i].attrib) for i in range(len(item))]
        for item in interesting_pomp
    ]
    for item in val[:3]:
        print(parser(item))


else:
    import manage_data
