import xml.etree.ElementTree as ET
import urllib.request
import sys
from time import strftime, localtime

schedule_url = "https://www.pgcon.org/2018/schedule/schedule.en.xml"
print( "## getting meta data from " + schedule_url + " ##")
global frab_data
try:
    frab_data = urllib.request.urlopen(schedule_url)
except:
    print( "Could not load schedule xml. Please check url")
    sys.exit(1)

tree = ET.parse(frab_data)
root = tree.getroot()

download_time = localtime()
formatted_download_time = strftime("%Y-%m-%d %H:%M", download_time)

root.append(ET.Element('version'))
root.find('version').text = formatted_download_time

for day in root.iter('day'):
    date = day.attrib['date']
    day.set('end', date + "T05:00:00-04:00")
    day.set('start', date + "T08:00:00-04:00")
    for event in day.iter('event'):
        # Append ISO 8601 date; example: 2016-02-29T23:42:00+01:00
        event.append(ET.Element('date'))
        event.find('date').text = date +  "T" + event.find('start').text + ":00-04:00"
        # event.find('date').text = date +  "T" + event.find('start').text + ":00+01:00"

# tree.write("schedule-" + strftime("%Y%m%d_%H%M", download_time) + ".xml")
tree.write("/home/opentree/html/pgcon2018/schedule.xml")

print( "## downloaded file from " + schedule_url + " ## " + strftime("%Y%m%d_%H%M", download_time))