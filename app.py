from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Get user inputs
        electric_bill = float(request.form.get('electric_bill'))
        gas_bill = float(request.form.get('gas_bill'))
        fuel_bill = float(request.form.get('fuel_bill'))

        total_waste = float(request.form.get('total_waste'))
        recycled_waste = float(request.form.get('recycled_waste')) / 100

        business_travel = float(request.form.get('business_travel'))
        fuel_efficiency = float(request.form.get('fuel_efficiency'))

        # Carbon Footprint Calculations
        energy_footprint = (electric_bill * 12 * 0.0005) + (gas_bill * 12 * 0.0053) + (fuel_bill * 12 * 2.32)
        waste_footprint = (total_waste * 12) * (0.57 - recycled_waste)
        travel_footprint = (business_travel * (1 / fuel_efficiency)) * 2.31
        total_footprint = energy_footprint + waste_footprint + travel_footprint

        #Suggestions
        suggestions = []
        if energy_footprint > 100:
            suggestions.append("💡 Reduce electricity usage by switching to LED bulbs and energy-efficient appliances.")
        if waste_footprint > 50:
            suggestions.append("♻️ Try recycling more and reducing single-use plastics.")
        if travel_footprint > 200:
            suggestions.append("🚗 Consider carpooling or using public transportation to reduce emissions.")

        # Save BarChart
        categories = ["Energy", "Waste", "Travel"]
        values = [energy_footprint, waste_footprint, travel_footprint]

        plt.figure(figsize=(6, 4))
        plt.bar(categories, values, color=['blue', 'green', 'red'])
        plt.xlabel("Category")
        plt.ylabel("CO₂ Emissions (kg)")
        plt.title("Your Carbon Footprint Breakdown")
        chart_path = os.path.join("static", "chart.png")
        plt.savefig(chart_path)
        plt.close()

        return render_template('result.html',
                               energy_footprint=round(energy_footprint, 2),
                               waste_footprint=round(waste_footprint, 2),
                               travel_footprint=round(travel_footprint, 2),
                               total_footprint=round(total_footprint, 2),
                               suggestions=suggestions,
                               chart_path=chart_path)

    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
