from retrieve_data import *
from calculations import *
from revenue_graph import *


class Stock:
	def __init__(self, stock_ticker):
		self.stock_ticker = stock_ticker
		self.retrieve_data = RetrieveData(stock_ticker)
		self.stock_data = self.retrieve_data.get_all_data()
		self.calculations = Calculations(self.stock_data)
		self.revenue_graph = None

	def create_revenue_graph(self):
		self.revenue_graph = RevenueGraph(self)