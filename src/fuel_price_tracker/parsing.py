import os
from types import prepare_class
import xml.etree.ElementTree as ET
import argparse
import manage_data


sorting_by_price = True

parser = argparse.ArgumentParser()
parser.add_argument("--dept", help="french departement number to process")
parser.add_argument("--gas", help="king of fuel to process")

args = parser.parse_args()
import dotenv
import smtplib


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
        string = "---------------------------\n"
        d = {}
        for key, value, data, index in zip(
            self.tag_list, self.text_list, self.attrib_list, range(len(self.tag_list))
        ):

            if key == "services":
                string += f"""{key} : {', '.join([self.node[index][i].text for i
                in range(len(self.node[index]))])}\n"""
                d.update(
                    {
                        key: {
                            ", ".join(
                                [
                                    self.node[index][i].text
                                    for i in range(len(self.node[index]))
                                ]
                            )
                        }
                    }
                )
            elif key == "prix":
                string += f"""{key} : {data['nom']} : {data['valeur']} € (dernière mise à jour {data['maj']})\n"""
                d.update({key + "_" + data["nom"]: (data["valeur"], data["maj"])})
            elif data == {}:
                d.update({key: value})
                string += f"""{key} : {value}\n"""
            else:
                d.update({key: (value, data)})
                string += f"""{key} : {value}
                                    {data}\n"""

        return string, d


tree = ET.parse("../../data/PrixCarburants_instantane.xml")
root = tree.getroot()
#  = sorted(interesting_pomp, key=lambda student: student[2])
interesting_pomp = [
    Pomp(item).info()[1] for item in root if item.attrib["cp"][:2] == args.dept
]

if sorting_by_price:
    interesting_pomp = [
        item for item in interesting_pomp if "prix_" + str(args.gas) in item.keys()
    ]
    interesting_pomp = sorted(
        interesting_pomp, key=lambda dict: dict["prix_" + str(args.gas)]
    )


dotenv.load_dotenv()

sender = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

receivers = [os.getenv("ADRESS_1"), os.getenv("ADRESS_2"), os.getenv("ADRESS_3")]

smtp_serv = os.getenv("SERVER")
port = 587
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content(str(interesting_pomp))

msg[
    "Subject"
] = f"Prix carburants ({args.gas}) dans le {args.dept} aujourd'hui (du - chère au + chère)"
msg["From"] = os.getenv("EMAIL")
msg["To"] = ", ".join(receivers)


with smtplib.SMTP(smtp_serv, port) as server:
    server.login(sender, password)
    server.set_debuglevel(1)
    server.send_message(msg)