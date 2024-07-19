import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime
import re

# URL of the calendar page
url = 'https://medical-tribune.co.jp/gakkai/gkcalendar/'

# Send a GET request to the URL
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# Find the calendar entries
events = soup.select('.event-entry')  # Adjust the selector based on the actual HTML structure

# Create a new calendar
cal = Calendar()

for event in events:
    summary = event.select_one('.event-title').text.strip()
    date_str = event.select_one('.event-date').text.strip()
    
    # Extract start and end dates
    date_match = re.match(r'(\d{4}.\d{2}.\d{2})-(\d{4}.\d{2}.\d{2})', date_str)
    if date_match:
        start_date = datetime.strptime(date_match.group(1), '%Y.%m.%d')
        end_date = datetime.strptime(date_match.group(2), '%Y.%m.%d')
    else:
        start_date = datetime.strptime(date_str, '%Y.%m.%d')
        end_date = start_date

    # Create a new event
    event = Event()
    event.add('summary', summary)
    event.add('dtstart', start_date)
    event.add('dtend', end_date)
    cal.add_component(event)

# Save the calendar to an .ics file
with open('calendar.ics', 'wb') as f:
    f.write(cal.to_ical())

print("iCal file has been created.")
