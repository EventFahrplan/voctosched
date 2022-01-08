import xml.etree.ElementTree as ET
import urllib.request
import sys
from time import strftime, localtime

schedule_url = "https://fosdem.org/2023/schedule/xml"
time_zone_name = "Europe/Brussels"
print("## getting meta data from " + schedule_url + " ##")
global frab_data
try:
    frab_data = urllib.request.urlopen(schedule_url)
except:
    print("Could not load schedule xml. Please check url")
    sys.exit(1)

tree = ET.parse(frab_data)
root = tree.getroot()

download_time = localtime()
formatted_download_time = strftime("%Y-%m-%d %H:%M", download_time)

root.append(ET.Element('version'))
root.find('version').text = formatted_download_time

conference = root.find('conference')
conference.append(ET.Element('time_zone_name'))
conference.find('time_zone_name').text = time_zone_name

for day in root.iter('day'):
    date = day.attrib['date']
    day.set('end', date + "T05:00:00+01:00")
    day.set('start', date + "T10:00:00+01:00")
    for event in day.iter('event'):
        # Append ISO 8601 date; example: 2016-02-29T23:42:00+01:00
        event.append(ET.Element('date'))
        event.find('date').text = date + "T" + event.find('start').text + ":00+01:00"

# Local test with time stamp suffix
# tree.write("schedule-" + strftime("%Y%m%d_%H%M", download_time) + ".xml")

# Production path
# tree.write("/home/metadude/html/fosdem2023/schedule.xml")

# Log output
print("## downloaded file from " + schedule_url + " ## " + strftime("%Y%m%d_%H%M", download_time))
