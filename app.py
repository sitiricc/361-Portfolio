from flask import Flask, render_template, request
from current_weather import get_weather

app = Flask(__name__)

def celsius_to_fahrenheit(celsius_temp):
    return round((celsius_temp * 9/5) + 32, 1)

@app.route('/', methods=["GET", "POST"])
def index():
    """ For the index file. """
    data = None
    if request.method == "POST":
        city= request.form["city"]
        state= request.form["state"]
        country= request.form["country"]
        
        with open('location.txt', 'w') as f:
            f.write(f"{city}, {state}, {country}")
        
        data_list = get_weather()
        
        
        if data_list:
            data = {
                'temperature': data_list[0].get('current_temp_fahrenheit'),
                'humidity': data_list[1].get('humidity'),
                'description': data_list[2].get('description'),
                'icon': data_list[3].get('icon')
            }

            
            data['temperature_fahrenheit'] = celsius_to_fahrenheit(data['temperature'])
    return render_template("index.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
