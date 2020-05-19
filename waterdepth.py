""" Download and format hydrology data from the USGS at water.weather.gov.
Read and parse the data from the XML tree and compare to flood data.
If data is not available, report a download error.

Author: Tyler Bongers
Last modified: 19 May 2020
"""

import xml.etree.ElementTree as ET
import urllib.request as url


def download(address='https://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=elnm4&output=xml'):
	""" Download the most recent page; defaults to the Red Cedar River at East Lansing MI """
	print('Fetching page from water.weather.gov')

	try:
		return url.urlopen(address)
	except:
		print('Page unavailable')
		return 0
		
def get_data(page):
	""" Format the data from the XML tree and report it """
	# This trusts that the XML tree is formatted well
	tree = ET.parse(page)
	root = tree.getroot()
	
	time = ' '.join(root.attrib['generationtime'].split('T'))
	print(f'\nGeneration time: {time} UTC	')
	
	try:
		river, location = root.attrib['name'].split('AT')
	
		# Trim extra whitespace
		while river[-1] == ' ':
			river = river[:-1]
		while location[0] == ' ':
			location = location[1:]
		print(f'Location: {river}, {location}\n')
	except:
		river = root.attrib['name']
		print(f'Location: {river}\n')
		
	# Parse the XML tree and get the basic information
	for child in root.iter():
	
		# Flood staging data
		if child.tag == 'sigstages':
			stages = {stage.tag:float(stage.text) for stage in child}
			
		# Look for the most recent observation; find it and break
		if child.tag == 'observed':
			for observation in child.iter('datum'):
				for d in observation.iter():

				# 'primary' keeps river depth and units
				# 'valid' has the reporting time
				# 'secondary' has outflow volume
					
					if d.tag == 'valid':
						zone = d.attrib['timezone']
						time = ' '.join(d.text.split('T'))
						print(f'Observation time: {time} {zone}')
						
					if d.tag == 'primary':
						depth = d.text
						units = d.attrib['units']
						print(f'River depth: {depth} {units}')
					
			
				# Found the observation, so break
				break
			
	# Flood alert information -- compare to the stage information found earlier
	depth = float(depth)		# Hehe
	if depth > stages['record']:
		s = stages['record']
		print(f'River is at record flood stage -- above {s} {units}')
	elif depth > stages['major']:
		s = stages['major']
		print(f'River is at major flood stage -- above {s} {units}')
	elif depth > stages['moderate']:
		s = stages['moderate']
		print(f'River is at moderate flood stage -- above {s} {units}')
	elif depth > stages['flood']:
		s = stages['flood']
		print(f'River is at flood stage -- above {s} {units}')
	elif depth > stages['bankfull']:
		s = stages['bankfull']
		print(f'River is at bankfull stage -- above {s} {units}')
	elif depth > stages['action']:
		s = stages['action']
		print(f'River is at action stage -- above {s} {units}')
		

addresses = {'RedCedar':'https://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=elnm4&output=xml',
	'GrandRiver':'https://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=lnsm4&output=xml',
	'SycamoreCreek':'https://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=hhtm4&output=xml'}
# Some default data

if __name__ == '__main__':
	page = download()
	if page:
		get_data(page)