import tkinter as tk
from tkinter import simpledialog, Tk, ttk, Scale, Label, HORIZONTAL, Frame
from stock import Stock


class Display:
	def __init__(self):
		self.stock = None
		self.root = tk.Tk()
		self.root.geometry("800x800")
		self.root.title("Stock DCF Analysis")


		# GUI Elements
		label = ttk.Label(self.root, text="Enter Stock Ticker:")
		label.pack(pady=10)

		self.entry = ttk.Entry(self.root)
		self.entry.pack(pady=5)

		button = ttk.Button(self.root, text="Analyze", command=self.analyze_stock) # self.analyze_stock
		button.pack(pady=10)

		self.create_menu()
		self.center_window()


	def create_menu(self):
		# Create a menu bar
		menubar = tk.Menu(self.root)
		self.root.config(menu=menubar)

		# Create Graph menu
		graph_menu = tk.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Menu", menu=graph_menu)

		# Create a submenu for Revenue under Graph
		revenue_menu = tk.Menu(graph_menu, tearoff=0)
		graph_menu.add_cascade(label="Graphs", menu=revenue_menu)

		# Add command to the Revenue submenu
		revenue_menu.add_command(label="Show Revenue Graph", command=self.show_revenue_graph) #self.show_revenue_graph


	def show_results(self, results):
		# Display the results in a grid format with a box around it
		frame = Frame(self.root, borderwidth=2, relief="solid")  # Add a box around the grid
		frame.pack(pady=20)

		headers = ["Metric", "Value"]
		metrics = ["Cost of Equity (CAPM)", "WACC", "Terminal Value", "DCF", "Share Value"]

		# Format the values appropriately
		values = [
			f"{results['cost_of_equity'] * 100:.2f}%",  # CAPM displayed as a percentage
			f"{results['wacc'] * 100:.2f}%",  # WACC displayed as a percentage
			f"${results['terminal_value'] / 1e6:,.2f} MM",  # Terminal Value in millions
			f"${results['dcf_value'] / 1e6:,.2f} MM",  # DCF in millions
			f"${results['share_value']:,.2f}"  # Share Value (cost per share)
		]

		# Create headers
		for i, header in enumerate(headers):
			label = ttk.Label(frame, text=header, font=('Arial', 10, 'bold'))
			label.grid(row=0, column=i, padx=10, pady=5)

		# Create metric and value rows
		for i, metric in enumerate(metrics):
			metric_label = ttk.Label(frame, text=metric)
			value_label = ttk.Label(frame, text=values[i])
			metric_label.grid(row=i + 1, column=0, padx=10, pady=5)
			value_label.grid(row=i + 1, column=1, padx=10, pady=5)

	def center_window(self):
		self.root.update_idletasks()
		w = self.root.winfo_width()
		h = self.root.winfo_height()
		x = (self.root.winfo_screenwidth() // 2) - (w // 2)
		y = (self.root.winfo_screenheight() // 2) - (h // 2)
		self.root.geometry(f'{w}x{h}+{x}+{y}')

	def run(self):
		self.root.mainloop()

	def show_revenue_graph(self):
		# Clear previous scene
		for widget in self.root.winfo_children():
			widget.destroy()

		# Re-create GUI elements for stock analysis
		label = ttk.Label(self.root, text="Enter Stock Ticker:")
		label.pack(pady=10)

		self.entry = ttk.Entry(self.root)
		self.entry.pack(pady=5)

		button = ttk.Button(self.root, text="Analyze", command=self.analyze_stock)
		button.pack(pady=10)

		# Display the revenue graph if stock data is available
		if self.stock:
			self.stock.create_revenue_graph()

		self.center_window()

	def ask_user_for_missing_data(self, missing_values):
		# Prompt the user to fill in missing values via a pop-up dialog
		data = {}
		for key, unit in missing_values.items():
			value = simpledialog.askfloat(f"Input {key}", f"Please enter the {key} ({unit}):")
			if value is not None:
				# Convert percentages (e.g. 18 -> 0.18) and handle unit adjustments
				if unit == "percentage":
					value = value / 100
				elif unit == "billions":
					value = value * 1e9
				elif unit == "millions":
					value = value * 1e6
				data[key] = value
		return data

	def analyze_stock(self):
		self.stock_ticker = self.entry.get()
		self.stock = Stock(self.stock_ticker)  # Store stock instance

		# Check for missing data
		missing_data = {}
		equity = self.stock.retrieve_data.get_equity()
		if equity is None:
			missing_data["Equity"] = "billions"
		debt = self.stock.retrieve_data.get_debt()
		if debt is None:
			missing_data["Debt"] = "billions"
		cost_of_debt = self.stock.retrieve_data.get_cost_of_debt()
		if cost_of_debt is None:
			missing_data["Cost of Debt"] = "percentage"
		tax_rate = self.stock.retrieve_data.get_tax_rate()
		if tax_rate is None:
			missing_data["Tax Rate"] = "percentage"

		if missing_data:
			user_inputs = self.ask_user_for_missing_data(missing_data)
			equity = user_inputs.get("Equity", equity)
			debt = user_inputs.get("Debt", debt)
			cost_of_debt = user_inputs.get("Cost of Debt", cost_of_debt)
			tax_rate = user_inputs.get("Tax Rate", tax_rate)

		# DCF Calculation (example values for CAPM and WACC inputs)
		calc = self.stock.calculations

		# Example values for CAPM and WACC inputs
		risk_free_rate = 0.03  # 3%
		beta = 1.2
		market_return = 0.08  # 8%

		cost_of_equity = calc.calculate_capm(risk_free_rate, beta, market_return)

		# Estimate projected cash flows (example values)
		free_cash_flow = self.stock.stock_data['free_cash_flow'] if self.stock.stock_data[
			'free_cash_flow'] else 1000000  # Use default if missing
		growth_rate = 0.05  # Assume 5% growth
		projected_cash_flows = calc.estimate_cash_flows(free_cash_flow, growth_rate)

		# Calculate WACC
		wacc = calc.calculate_wacc(equity, debt, cost_of_equity, cost_of_debt, tax_rate)

		# Terminal value calculation
		terminal_growth = 0.03  # 3%
		fcf_year_5 = projected_cash_flows[-1]
		terminal_value = calc.calculate_terminal_value(fcf_year_5, terminal_growth, wacc)

		# DCF value calculation
		dcf_value = calc.calculate_total_dcf(projected_cash_flows, fcf_year_5, terminal_growth, wacc)

		shares_outstanding = self.stock.retrieve_data.get_shares_outstanding()

		dcf_share_value = calc.calculate_dcf_share_value(dcf_value, shares_outstanding)

		# Display results
		results = {
			"cost_of_equity": cost_of_equity,
			"wacc": wacc,
			"terminal_value": terminal_value,
			"dcf_value": dcf_value,
			"share_value": dcf_share_value
		}

		self.show_results(results)


