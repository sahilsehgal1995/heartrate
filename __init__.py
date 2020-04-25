# importing the requests library 
import flask
from flask import request, make_response
import requests 
from datetime import datetime
import flask_excel as excel
import itertools

app = flask.Flask(__name__)
excel.init_excel(app)
app.config["DEBUG"] = True

def getData(URL):  
	# sending get request and saving the response as response object 
	r = requests.get(url = URL) 
	data = r.json() 
	return data['cardiogram']['cards'][0]['song']['lines']['heartRate']['_line']

@app.route('/', methods=['GET'])
def home():
	try:
		heartRates = getData(request.args.get('url'))
		
		for heartRate in heartRates:
			heartRate['start'] = datetime.fromtimestamp(heartRate['start']/1000.0)
			heartRate['end'] = datetime.fromtimestamp(heartRate['end']/1000.0)

		dataset = []
		for heartRate in heartRates:
		    heartRate['timestamp'] = heartRate['start'].strftime("%H:%M")
		    heartRate['heart_beat'] = (int(heartRate['value']/10)*10)
		    dataset.append([heartRate['timestamp'], heartRate['heart_beat']])

		dataset.sort()
		dataset = list(dataset for dataset,_ in itertools.groupby(dataset))

		return excel.make_response_from_array(dataset, "csv", file_name="heart.csv")
	except Exception as e:
		return str(e)


app.run()