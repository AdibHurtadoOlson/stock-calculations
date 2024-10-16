from matplotlib import pyplot as plt
from tkinter import Tk, Scale, Label, HORIZONTAL, Frame

class RevenueGraph:
	def __init__(self, stock_instance):
		self.stock_instance = stock_instance
		self.historical_revenue = self.stock_instance.stock_data['income_statement'].loc['Total Revenue'].tolist()[-4:]  # Last 4 years historical
		self.projected_revenue = [self.historical_revenue[0]] * 5  # Placeholder for projections (2025-2029)
		self.create_graph_window()

	def create_graph_window(self):
		# Create revenue graph window with sliders
		graph_window = Tk()
		graph_window.title(f'Revenue Graph for {self.stock_instance.stock_ticker}')
		graph_window.geometry("500x700")

		# Create a frame for sliders
		frame = Frame(graph_window)
		frame.pack(pady=10)

		# Create sliders for individual years (2025-2029)
		for i in range(5):
			year = 2025 + i
			label = Label(frame, text=f'Estimate for {year}:', font=("Arial", 12))
			label.pack(pady=5)

			year_slider = Scale(frame, from_=-50, to=50, resolution=1, orient=HORIZONTAL,
								command=lambda val, index=i: self.on_individual_estimate_change(index, val),
								length=400)
			year_slider.set(0)  # Starts at 0% change
			year_slider.pack(pady=5)
			setattr(self, f"year_slider_{i}", year_slider)

		# Initial graph display
		self.update_graph()

		graph_window.mainloop()

	def update_graph(self):
		# Prepare revenue values to display
		historical_years = list(range(2021, 2025))[::-1]  # Reversed historical years: 2024, 2023, 2022, 2021
		projected_years = list(range(2025, 2030))

		# Combine historical and projected revenue
		revenue_values = self.historical_revenue + self.projected_revenue  # Reverse historical revenues

		# Convert values to billions for better display
		revenue_values_billions = [value / 1_000_000_000 for value in revenue_values]

		# Clear the existing plot and plot new bars
		plt.clf()

		# Plot the historical and projected revenue
		self.bars = plt.bar(historical_years + projected_years, revenue_values_billions[:len(historical_years + projected_years)], 
							color=['steelblue'] * len(historical_years) + ['lightgreen'] * len(projected_years))

		plt.xlabel('Years', fontsize=12)
		plt.ylabel('Revenue (Billion USD)', fontsize=12)
		plt.title(f'Revenue for {self.stock_instance.stock_ticker}', fontsize=14)
		plt.xticks(historical_years + projected_years, rotation=45, fontsize=10)
		plt.yticks(fontsize=10)
		plt.grid(axis='y', linestyle='--', alpha=0.7)
		plt.tight_layout()

		# Add revenue values above each bar
		for bar, value in zip(self.bars, revenue_values_billions):
			plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{value:.2f}', 
					 ha='center', va='bottom', fontsize=10, color='black')

		# Show the graph
		plt.show(block=False)


	def calculate_future_revenue(self):
		# Calculate future revenue based on percentage changes and historical revenue
		for i in range(5):
			previous_year_revenue = self.projected_revenue[i - 1] if i > 0 else self.historical_revenue[0]
			percent_change = getattr(self, f"year_slider_{i}").get()  # Get percentage change
			self.projected_revenue[i] = previous_year_revenue * (1 + percent_change / 100)  # Adjust for percentage change

	def on_individual_estimate_change(self, index, value):
		# Update projected revenue when an individual slider changes
		self.calculate_future_revenue()
		self.update_graph()


