import yfinance as yf
from matplotlib import pyplot as plt
from tkinter import simpledialog, Tk, ttk, Scale, Label, HORIZONTAL, Frame


class RetrieveData:
	def __init__(self, stock_ticker):
		self.stock_ticker = stock_ticker
		self.current_price = yf.Ticker(stock_ticker).info.get('currentPrice')
		self.data = self.get_financial_data()

	def get_financial_data(self):
		stock = yf.Ticker(self.stock_ticker)

		financials = {
						"income_statement": stock.financials,
			"cash_flow": stock.cashflow,
			"balance_sheet": stock.balance_sheet,
			"shares_outstanding": stock.info.get('sharesOutstanding'),
			"current_price": self.current_price,
			"free_cash_flow": stock.cashflow.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in stock.cashflow.index else None
		}

		return financials

	def get_equity(self):
		shares = self.get_shares_outstanding()
		price = self.current_price

		if shares is not None and price is not None:
			return shares * price
		return None

	def get_shares_outstanding(self):
		shares = self.data['shares_outstanding']
		if shares is not None:
			return shares
		else:
			return self.get_user_input("Shares outstanding data is missing. Please enter the number of shares outstanding:")


	def get_current_price(self):
		price = self.current_price
		if price is not None:
			return price
		else:
			return self.get_user_input("Current price data is missing. Please enter the current stock price:")

	def get_debt(self):
		balance_sheet = self.data['balance_sheet']
		debt_keys = ['Total Debt', 'Long Term Debt', 'Short Term Debt']
		for key in debt_keys:
			if key in balance_sheet.index:
				return balance_sheet.loc[key].iloc[0]
		return self.get_user_input("Debt data is missing. Please provide total debt amount:")

	def get_cost_of_debt(self):
		income_statement = self.data['income_statement']
		interest_expense = income_statement.loc['Interest Expense'].iloc[0] if 'Interest Expense' in income_statement.index else None
		total_debt = self.get_debt()

		if interest_expense is not None and total_debt is not None and total_debt > 0:
			return interest_expense / total_debt
		return None

	def get_tax_rate(self):
		income_statement = self.data['income_statement']
		income_before_tax = income_statement.loc['Income Before Tax'].iloc[0] if 'Income Before Tax' in income_statement.index else None
		tax_provision = income_statement.loc['Tax Provision'].iloc[0] if 'Tax Provision' in income_statement.index else None

		if income_before_tax is not None and tax_provision is not None:
			return tax_provision / income_before_tax
		return self.get_user_input("Tax rate data is missing. Please provide effective tax rate as a decimal (e.g., 0.21 for 21%):")

	def get_user_input(self, prompt):
		root = Tk()
		root.withdraw()  # Hide the root window
		user_input = simpledialog.askstring("Input Required", prompt)
		root.destroy()
		return float(user_input) if user_input and user_input.replace('.', '', 1).isdigit() else None

	def get_all_data(self):
		return self.data

