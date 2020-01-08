import json
import pandas
import time
import requests
from . import utils


class Smya:
    config = None
    stopper = None

    def __init__(self):
        # initialize config
        self.config = utils.loadConfig()

    def getStocks(self):
        """
      List all available stocks in stock file
    """
        stockFilePath = self.config["stock_file_path"]
        allStocks = pandas.read_csv(stockFilePath, usecols=[0, 1, 2, 3, 4])
        # convert csv to dict
        allStock = allStocks.to_dict(orient="records")
        # todo: improve approach
        self.stopper = int(len(allStock))
        return allStock

    def generateLinks(self, stocks):
        i = 0
        print("Getting now all Links of the stocks:")
        for x in stocks:
            if i == self.stopper:
                break
            else:
                wknnr = stocks[i].get("WKN")
                if len(wknnr) is 6:
                    pass
                else:
                    print("no WKN number")
                    break
                url = "https://www.onvista.de/"
                isbnurl = url + wknnr
                time.sleep(1)
                r = requests.get(isbnurl)
                ##sleep(randint(3, 7))
                link = r.url
                stocks[i].update({"Link": link})
                i += 1
                print(link)

        i = 0
        for x1 in stocks:
            if i == self.stopper:
                i = 0
                break
            else:
                url = stocks[i].get("Link")
                linkvista = url.rsplit("/", 1)[-1]
                isbn = url.rsplit("-", 1)[-1]
                print("Before we get all Links we check if the WKN is a valid isbn")
                if utils.checkIsbn(isbn) is True:
                    print("Damn this looks like a isbn, lets rock!")
                    print(
                        "Now updating the Links to formated names and numbers"
                        + linkvista
                    )
                    stocks[i].update({"Onvistaname": linkvista})
                else:
                    continue
                i += 1

        i = 0
        print("Now getting all fundamentallinks for the stocks")
        for x2 in stocks:
            if i == self.stopper:
                i = 0
                break
            else:
                company = str(stocks[i].get("Onvistaname"))
                fundamental_data_url = (
                    "https://www.onvista.de/aktien/fundamental/" + company
                )
                stocks[i].update({"Fundamentaldatenlink": fundamental_data_url})
                i += 1
                print(fundamental_data_url)

        return stocks
