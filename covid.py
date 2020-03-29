import requests
import matplotlib.pyplot as plt
import datetime
import numpy as np
import sys



def get_field_as_array(json_data, field):
	arr = [d.get(field) if d.get(field) else 0 for d in json_data]
	return arr

def get_zipped_arrays(json_data, fields):
	arrays = [get_field_as_array(json_data, f) for f in fields]
	return arrays

def plot_data(title, json_data):

	unparsed_dates = get_zipped_arrays(json_data, ['date'])[0]
	dates = [parse_date(d) for d in unparsed_dates]
	positives, total_tests, negatives, hospitalized, deaths = get_zipped_arrays(json_data, ['positive', 'totalTestResults', 'negative', 'hospitalized', 'deaths'])
	deathIncrease, hospitalizedIncrease, negativeIncrease, positiveIncrease, totalTestResultsIncrease,= get_zipped_arrays(json_data, ['deathIncrease', 'hospitalizedIncrease', 'negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease'])
	fig=plt.figure(figsize=(14,8))
	fig.suptitle(title, fontsize=14)
	ax = plt.subplot(121)

	ax.bar(dates, total_tests, color='b', label='Total Tests')
	ax.bar(dates, negatives, color ='g', label = 'Negative Tests')
	ax.bar(dates, positives, color='y',label = 'Positive Tests')
	ax.bar(dates, hospitalized, color='r',label = 'Total Hospitalized')

	ax.bar(dates, deaths, color='k',label = 'Total Deaths')
	ax.xaxis_date()

	ax.legend()
	plt.title("Covid-19 Testing Totals", loc='center')

	ax2 = plt.subplot(122)


	ax2.xaxis_date()
	ax2.plot_date(dates, deathIncrease, 'k', label = 'Death Increase')
	ax2.plot_date(dates, hospitalizedIncrease, 'r', label = 'Hospitalized Increase')

	ax2.plot_date(dates, negativeIncrease, 'g', label = 'Negative Increase')

	ax2.plot_date(dates, positiveIncrease, 'y', label = 'Positive Increase')
	ax2.plot_date(dates, totalTestResultsIncrease, 'b', label = 'totalTestResultsIncrease')

	ax2.legend()

	plt.title("Covid-19 Testing Daily Changes", loc='center')
	for label in ax.xaxis.get_ticklabels()[::2]:
		label.set_visible(False)
	for label in ax2.xaxis.get_ticklabels()[::2]:
		label.set_visible(False)
	plt.show()


def generate_plots(y_arrays, rows=4, cols=3):
	axis = []
	print(len(y_arrays))
	for a in range(1, len(y_arrays)):
		axis.append(plt.subplot(rows,cols,a))
	return axis


def parse_date(unparsed):
	parsed = datetime.datetime.strptime(str(unparsed), '%Y%m%d').date()
	return parsed

def plot_array(axis, x, y_arrays, labels):

	for ax, y, lab,in zip(axis, y_arrays, labels):

		if 'negative' in lab or 'totalTestResults' in lab:
			col = 'g'
		elif 'positive' in lab or 'death' in lab or 'hospitalized' in lab:
			col = 'r'
		else:
			col = 'b'			

		ax.bar(x, y, color=col, label=lab)

		ax.xaxis_date()
		for label in ax.xaxis.get_ticklabels()[::2]:
			label.set_visible(False)
		ax.legend()


def many_plots(data, title,labels):
	fig = plt.figure(figsize=(14,8))
	fig.suptitle(title, fontsize=14)
	arrays = get_zipped_arrays(data, ['date', 'positive', 'negative', 'posNeg', 'pending', 'hospitalized', 'death', 'totalTestResults', 'deathIncrease', 'hospitalizedIncrease', 'negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease'])
	axis = generate_plots(arrays[1:])
	dates = [parse_date(d) for d in arrays[0]]
	plot_array(axis, dates, arrays[1:],labels )
	plt.show()

def main():
	region = sys.argv[1].lower()
	if region == 'tx' or region == 'texas':
		title = "Texas Covid-19"
		url = "https://covidtracking.com/api/states/daily?state=TX"
	elif region == 'ny'or region == 'new york':
		title = "New York Covid-19"

		url = "https://covidtracking.com/api/states/daily?state=NY"
	else:
		title = "USA Covid-19"

		url = "https://covidtracking.com/api/us/daily"

	data_daily = requests.get(url).json()
	posrate = float(data_daily[0]['positive']/data_daily[0]['totalTestResults'])
	print(posrate)
	plot_data(title, data_daily)



if __name__ == '__main__':
	main()