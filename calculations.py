


class Calculations:
	def __init__(self, stock_data):
		self.stock_data = stock_data

	def calculate_capm(self, risk_free_rate, beta, market_return):
		# Calculate the expected return based on CAPM
		return risk_free_rate + beta * (market_return - risk_free_rate)

	def calculate_wacc(self, equity, debt, cost_of_equity, cost_of_debt, tax_rate):
		# Calculate the Weighted Average Cost of Capital (WACC
		total_value = equity + debt
		return (equity / total_value) * cost_of_equity + (debt / total_value) * cost_of_debt * (1 - tax_rate)

	def calculate_terminal_value(self, fcf_year_5, terminal_growth, discount_rate):
		# Calculate terminal value based on free cash flow, growth, and discount rate
		return fcf_year_5 * (1 + terminal_growth) / (discount_rate - terminal_growth)

	def calculate_dcf(self, cash_flows, discount_rate):
		# Calculate the Discounted Cash Flow (DCF
		return sum(cf / (1 + discount_rate) ** (i + 1) for i, cf in enumerate(cash_flows))

	def calculate_total_dcf(self, projected_cash_flows, fcf_year_5, terminal_growth, discount_rate):
		# Calculate the total DCF value including terminal value
		dcf_value = self.calculate_dcf(projected_cash_flows, discount_rate)
		terminal_value = self.calculate_terminal_value(fcf_year_5, terminal_growth, discount_rate)
		return dcf_value + (terminal_value / (1 + discount_rate) ** len(projected_cash_flows))

	def predict_financials(self, years=5):
		historical_revenue = self.stock_data['income_statement'].loc['Total Revenue']
		historical_revenue = historical_revenue.iloc[0:years]  # Get historical revenue
		revenue_growth_rate = (historical_revenue.iloc[-1] / historical_revenue.iloc[0]) ** (1 / (years - 1)) - 1
		projected_revenue = [historical_revenue.iloc[-1] * (1 + revenue_growth_rate) ** i for i in range(1, years + 1)]
		return projected_revenue

	def estimate_cash_flows(self, free_cash_flow, growth_rate, years=5):
		return [free_cash_flow * (1 + growth_rate) ** i for i in range(years)]

	def calculate_dcf_share_value(self, total_dcf, shares_outstanding):
		# Calculate the DCF value per share
		return total_dcf / shares_outstanding if shares_outstanding > 0 else None