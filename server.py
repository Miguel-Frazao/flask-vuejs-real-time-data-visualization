#!/usr/bin/python3

# CREATE DUMMY DATA

# import pandas as pd
# from datetime import datetime, timedelta
# import random
# now = datetime.now()
# configs = {
# 	'Y1': (0, 250),
# 	'Y2': (0, 500),
# 	'Y3': (0, 750),
# }

# df_num_rows = 10000
# y_vals = {i: [random.randint(*configs[i]) for j in range(df_num_rows)] for i in configs}

# df = pd.DataFrame({
# 	'X': ['{:%Y-%m-%d %H:%M:%S}'.format(now + timedelta(seconds=i)) for i in range(df_num_rows)],
# 	**y_vals # ex: {**{'a': [1, 2, 3], 'b': [4, 5, 6]}}
# })

# df.to_csv('test_data.csv', index=False)

# API
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
	offset = request.args.get('offset', default = 1, type = int)
	limit = request.args.get('limit', default = 1, type = int)
	df = pd.read_csv('test_data.csv', skiprows=range(1, offset+1), nrows=limit, parse_dates=['X'])

	cols = [col for col in df.columns if col.startswith('Y')]

	configs = {
		'Y1': {'color': '#483D8B', 'col_name': 'name_Y1'},
		'Y2': {'color': '#f87979', 'col_name': 'name_Y2'},
		'Y3': {'color': '#00BFFF', 'col_name': 'name_Y3'},
	}

	datasets = []
	for k, c in enumerate(cols):
		datasets.append({
			'label': configs[c]['col_name'],
			'borderColor': configs[c]['color'],
			'backgroundColor': configs[c]['color'],
			'borderWidth': 2,
			'pointBorderColor': '#000000',
			'lineTension': k*0.23, # line curve
			'pointRadius': 2,
			'pointBorderWidth': 1,
			'fill': False,
			'data': df[c].tolist()
		})

	chart = {
		'labels': df['X'].dt.strftime('%H:%M:%S').tolist(),
		'datasets': datasets
	}

	return jsonify({'chart_data': chart})

app.run()
