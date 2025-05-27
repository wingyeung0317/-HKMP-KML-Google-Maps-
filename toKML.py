import json
import requests
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

# API URL and headers
url = "https://www.hkemobility.gov.hk/api/drss/layer/map/?typeName=DRSS%3AVW_ON_STREET_PARKING&service=WFS&version=1.0.0&request=GetFeature&outputFormat=application%2Fjson&styles=OSP_Type_ALL&cql_filter=(VEHICLE_TYPE%20%3D%20'Motor%20Cycles')%20AND%20BBOX(SHAPE%2C%20113.7715210770302%2C22.09149645255427%2C114.56486620617868%2C22.58284043586623)"

headers = {
    'Origin': 'https://www.hkemobility.gov.hk',
    'Referer': 'https://www.hkemobility.gov.hk/tc/toll-rate/'
}

# Fetch JSON data from API
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    data = response.json()
except requests.RequestException as e:
    print(f"Error fetching data from API: {e}")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    exit(1)

# Create KML structure
kml = Element('kml', xmlns="http://www.opengis.net/kml/2.2")
document = SubElement(kml, 'Document')

# Iterate through features and extract coordinates and STREET_NAME_TC
for feature in data['features']:
    coordinates = feature['geometry']['coordinates']
    street_name_tc = feature['properties']['STREET_NAME_TC']
    
    placemark = SubElement(document, 'Placemark')
    name = SubElement(placemark, 'name')
    name.text = street_name_tc
    
    point = SubElement(placemark, 'Point')
    coord = SubElement(point, 'coordinates')
    coord.text = f"{coordinates[0]},{coordinates[1]}"

# Write to KML file
tree = ElementTree(kml)
tree.write('motorcycleParking.kml', encoding='utf-8', xml_declaration=True)

print("KML file generated successfully: motorcycleParking.kml")