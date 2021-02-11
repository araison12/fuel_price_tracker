import os
from types import prepare_class
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
        string = "---------------------------\n"
        for key, value, data, index in zip(
            self.tag_list, self.text_list, self.attrib_list, range(len(self.tag_list))
        ):
            if key == "services":
                string += f"""{key} : {', '.join([self.node[index][i].text for i in range(len(self.node[index]))])}\n"""
            elif key == "prix":
                string += f"""{key} : {data['nom']} : {data['valeur']} € (dernière mise à jour {data['maj']})\n"""
            elif data == {}:
                string += f"""{key} : {value}\n"""
            else:
                string += f"""{key} : {value}
                                    {data}\n"""
        return string


tree = ET.parse("../../data/PrixCarburants_instantane.xml")
root = tree.getroot()
interesting_pomp = " ".join(
    [Pomp(item).info() for item in root if item.attrib["cp"][:2] == args.dept]
)

import dotenv
import smtplib
from email.mime.text import MIMEText

dotenv.load_dotenv()

sender = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
receivers = [os.getenv("ADRESS_1"), os.getenv("ADRESS_2"), os.getenv("ADRESS_3")]

smtp_serv = os.getenv("SERVER")
port = 465
msg = MIMEText(interesting_pomp)

msg["Subject"] = "Prix carburants de la vienne aujourd'hui"
msg["From"] = "services@adriorsn.eu"
msg["To"] = receivers

with smtplib.SMTP_SSL("localhost", port) as server:

    server.login(sender, password)
    for person in receivers:
        server.sendmail(sender, person, msg.as_string())
        print("Successfully sent email")