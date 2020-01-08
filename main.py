from app.Smya import Smya

smya = Smya()

stocks = smya.getStocks()
smya.generateLinks(stocks)
