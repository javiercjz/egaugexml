#!/usr/bin/env python
# Import libraries
import xml.etree.ElementTree as ET
import time
import gdata.spreadsheet.service
import requests
import json
import urllib2

email = 'jhondoe@gmail.com'
password = 'yourpassword'

# Find this value in the url with 'key=XXX' and copy XXX below
spreadsheet_key = 'Spreadsheet_Key'
# All spreadsheets have worksheets. I think worksheet #1 by default always
# has a value of 'od6'
worksheet_id = 'od6'

spr_client = gdata.spreadsheet.service.SpreadsheetsService()
spr_client.email = email
spr_client.password = password
spr_client.source = 'Egauge_Python'
spr_client.ProgrammaticLogin()

DROP = 0 

# Read data from Egauge
try:
        while True:
                # Import file from eGauge unit
                try:
                        file=urllib2.urlopen('http://egaugeXXXX.egaug.es/cgi-bin/egauge?inst')
                        data=file.read()
                        file.close()
                except:
                        DROP = DROP + 1
                        now=time.strftime('%Y-%m-%d %H:%M:%S')
                        print 'egauge unit unreachable, retrying in 30s'
                        print now
                        print 'Connection Drop Number: ',DROP
                        print
                        time.sleep(30)
                        continue
                # load File as Element
                root = ET.fromstring(data)
                powernow = root[2][1].text
                # Prepare the dictionary to write
                dict = {}
                dict['date'] = time.strftime('%m/%d/%Y')
                dict['time'] = time.strftime('%H:%M:%S')
                dict['powernow'] = powernow
                print dict

		try: 
			entry = spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)
			if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
                        	print "Insert row succeeded."
                	else:   
                        	print "Insert row failed."
		except:
			now=time.strftime('%Y-%m-%d %H:%M:%S')
			print 'export to google failed at: ',now
			print 'retrying again in 30s'
			print
			time.sleep(30)
			continue 			
                time.sleep(300)

except KeyboardInterrupt:
        print 'ctrl-c has been pressed, process aborted'

