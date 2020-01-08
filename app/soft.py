# -*- coding: utf-8 -*-
#
# GPLv3 thanks to Will Ayd, Rosettacode and my cold beer
#
# Feel free to donate for beer to becomebasti@gmail.com (paypal)
#
# CatchPi
#
import re
import requests
import datetime
import pandas as pd
import time as t
from random import randint
from time import sleep
from lxml import html
from pandas.io.json import json_normalize
import click

# stock page structure xpath
from .url import onvista_stock

# set filename and maybe path
c = False
csvname = "aktien.csv"

def load_cli():
    return True
    if c is True and click.confirm(
        "DO YOU NEED A GRAPHICAL INPUT FOR SELECTING THE CSV FILE?", default=True
    ):
        return True
    else:
        return False

print("Besure that there is ONE COLUMN with header: WKN")
if load_cli() is True:
    print("Press 1 or 2 to choose:")
    print("1: for uploading the file online. #easy")
    print("2: for selecting the path of the file on your computer.")
    choice = input("Enter your choice: ")
    choice = int(choice)
    if choice == 1:
        anon = "https://www.file.io/"
        print("Click here:    " + anon + "    and upload the csv...")
        url_to_get_file = input("Please now insert the URL with the csv file:")
        df = pd.read_csv(url_to_get_file, usecols=[0, 1, 2, 3, 4])
    else:
        stock_list_name = input("Enter the name of the file name WITHOUT .csv: ")
        t.sleep(2)
        path_to_file = input(
            "Enter the path to the file or leave it plain if file is in the app folder (Example: /home/user/document/)   "
        )
        filename = path_to_file + stock_list_name + ".csv"
        print(
            "We will set the first FIVE headers of the CSV to standard headers, MAKE SURE THERE IS ATLEAST ONE WKN COLUMN"
        )
        df = pd.read_csv(csvname, usecols=[0, 1, 2, 3, 4])
else:
    df = pd.read_csv(csvname)

result = df.to_dict(orient="records")
print(result)
stopper = int(len(result))


def stop():
    timeestimated = 6 * int(stopper) * 5
    print("To not get banned there are sleep limits so this process takes some time.")
    if timeestimated in range(60, 599):
        timeestimated = timeestimated / 60
        print(
            "This should take round about: "
            + str(round(timeestimated, 2))
            + " Minutes, so get a coffee and relax. DO NOT CLOSE THE WINDOW"
        )
    elif timeestimated >= 600:
        timeestimated = timeestimated / 3600
        print(
            "This should take round about: "
            + str(round(timeestimated, 2))
            + " Hours, so get a vegan burger, watch a nice video, safe energy and relax. DO NOT CLOSE THE WINDOW"
        )
    else:
        print(
            "This should take round about: "
            + str(round(timeestimated, 2))
            + " Seconds, so just watch and relax. DO NOT CLOSE THE WINDOW"
        )
    return stopper


def check(isbn):
    match = re.match(r"(\d)-(\d{3})-(\d{5})-(\d)$", isbn)
    if match:
        digits = [int(x) for x in "".join(match.groups())]
        check_digit = digits.pop()
        return (
            check_digit == sum([(i + 1) * digit for i, digit in enumerate(digits)]) % 11
        )
    return True


def link_generator():
    i = 0
    print("Getting now all Links of the stocks:")
    for x in result:
        if i == stopper:
            break
        else:
            wknnr = result[i].get("WKN")
            if len(wknnr) is 6:
                pass
            else:
                print("no WKN number")
                break
            url = "https://www.onvista.de/"
            isbnurl = url + wknnr
            t.sleep(1)
            r = requests.get(isbnurl)
            ##sleep(randint(3, 7))
            link = r.url
            result[i].update({"Link": link})
            i += 1
            print(link)

    i = 0
    for x1 in result:
        if i == stopper:
            i = 0
            break
        else:
            url = result[i].get("Link")
            linkvista = url.rsplit("/", 1)[-1]
            isbn = url.rsplit("-", 1)[-1]
            print("Before we get all Links we check if the WKN is a valid isbn")
            if check(isbn) is True:
                print("Damn this looks like a isbn, lets rock!")
                print(
                    "Now updating the Links to formated names and numbers" + linkvista
                )
                result[i].update({"Onvistaname": linkvista})
            else:
                continue
            i += 1

    i = 0
    print("Now getting all fundamentallinks for the stocks")
    for x2 in result:
        if i == stopper:
            i = 0
            break
        else:
            company = str(result[i].get("Onvistaname"))
            fundamental_data_url = (
                "https://www.onvista.de/aktien/fundamental/" + company
            )
            result[i].update({"Fundamentaldatenlink": fundamental_data_url})
            i += 1
            print(fundamental_data_url)

    return result


def stockanalysis(
    analysis_stockreturn=False,
    analysis_kgv=False,
    analysis_gewinnwachstum=False,
    analysis_divineuro=False,
    analysis_divinprozent=True,
):
    i = 0
    for x in result:
        if i == stopper:
            break
        else:
            company = str(result[i].get("Onvistaname"))
            fundamental_data_url = (
                "https://www.onvista.de/aktien/fundamental/" + company
            )
            pageContent = requests.get(fundamental_data_url)
            tree = html.fromstring(pageContent.content)
            if analysis_stockreturn is True:
                gewinn = []
                i1 = 0
                p = 1
                for i1 in range(4):
                    if i1 == 4:
                        break
                    else:
                        p += 1
                        ##sleep(randint(3, 7))
                        gewinn.append(
                            tree.xpath(
                                onvista_stock() + "[1]/tbody/tr[1]/td[" + str(p) + "]"
                                "/text()"
                            )
                        )
                        i1 += 1
                gewinn = ["".join(x) for x in gewinn]
                gewinn = [x.strip(" ") for x in gewinn]
                map(str.strip, gewinn)
                # gewinn = [x.encode('ascii', errors='replace') for x in gewinn]
                print(gewinn)
            else:
                gewinn = ["Not analysed"]

            if analysis_kgv is True:
                kgv = []
                i2 = 0
                p1 = 1
                for i1 in range(4):
                    if i2 == 4:
                        break
                    else:
                        p1 += 1
                        # sleep(randint(3, 7))
                        kgv.append(
                            tree.xpath(
                                onvista_stock()
                                + "[1]/tbody/tr[2]/td["
                                + str(p1)
                                + "]"
                                + "/text()"
                            )
                        )
                        i2 += 1
                kgv = ["".join(x) for x in kgv]
                kgv = [x.strip(" ") for x in kgv]
                map(str.strip, kgv)
                print(kgv)
            else:
                kgv = ["Not analysed"]

            if analysis_gewinnwachstum is True:
                gewinnwachstum = []
                i3 = 0
                p2 = 1
                for i1 in range(4):
                    if i3 == 4:
                        break
                    else:
                        p2 += 1
                        ##sleep(randint(3, 7))
                        gewinnwachstum.append(
                            tree.xpath(
                                onvista_stock()
                                + "[1]/tbody/tr[3]/td["
                                + str(p2)
                                + "]"
                                + "/text()"
                            )
                        )
                        i3 += 1
                gewinnwachstum = ["".join(x) for x in gewinnwachstum]
                gewinnwachstum = [x.strip(" ") for x in gewinnwachstum]
                map(str.strip, gewinnwachstum)
                print(gewinnwachstum)
            else:
                gewinnwachstum = ["Not analysed"]

            if analysis_divineuro is True:
                divineuro = []
                i4 = 0
                p3 = 1
                for i1 in range(4):
                    if i4 == 4:
                        break
                    else:
                        p3 += 1
                        # sleep(randint(3, 7))
                        divineuro.append(
                            tree.xpath(
                                onvista_stock()
                                + "[2]/tbody/tr[1]/td["
                                + str(p3)
                                + "]"
                                + "/text()"
                            )
                        )
                        i4 += 1
                divineuro = ["".join(x) for x in divineuro]
                divineuro = [x.strip(" ") for x in divineuro]
                map(str.strip, divineuro)
                print(divineuro)
            else:
                divineuro = ["Not analysed"]

            if analysis_divinprozent is True:
                divinprozent = []
                i5 = 0
                p4 = 1
                for i1 in range(4):
                    if i5 == 4:
                        break
                    else:
                        p4 += 1
                        # sleep(randint(3, 7))
                        divinprozent.append(
                            tree.xpath(
                                onvista_stock()
                                + "[2]/tbody/tr[2]/td["
                                + str(p4)
                                + "]"
                                + "/text()"
                            )
                        )
                        i5 += 1
                divinprozent = ["".join(x) for x in divinprozent]
                divinprozent = [x.strip(" ") for x in divinprozent]
                map(str.strip, divinprozent)
                print(divinprozent)
            else:
                divinprozent = ["Not analysed"]

        i6 = 0
        p5 = 3
        p6 = 3
        # four years - otherwise it would need more xpaths in the preceeding loops
        for i6 in range(4):
            if i6 == 4:
                break
            else:
                # year1 is year minus 1, year two is the year of execution, year 3 is year + 1 etc...
                now = datetime.datetime.now()
                year = []
                c = 0
                for c in range(4):
                    year.append(str(int(now.year) + 2 - c))
                    c += 1

                result[i].update(
                    {
                        year[p5]: {
                            "Gewinn pro Aktie": gewinn[(p6)],
                            "KGV": kgv[(p6)],
                            "Gewinnwachstum": gewinnwachstum[(p6)],
                            "Dividende in Euro": divineuro[(p6)],
                            "Dividende in Prozent": divinprozent[(p6)],
                        }
                    }
                )
                p5 = p5 - 1
                p6 = p6 - 1
                i6 += 1
        print("Fetching your stocks")
        print(result[i])
        i += 1

    return result


def output(c):
    if c is True:
        # Get the date object from datetime object
        date = pd.to_datetime("now")
        upload = "aktien_export_" + str(date) + ".csv"
        json_normalize(result).to_csv(upload)
        f = open(upload)
        r = requests.post(
            url="https://file.io", data={"title": upload}, files={"file": f}
        )
        json_response = r.json()
        print("Download your analysis")
        print(json_response['link'])
    else:
        json_normalize(result).to_csv("aktien_export.csv")

    return result
