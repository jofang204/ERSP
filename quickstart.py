from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
  import argparse
  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
  flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
  """Gets valid user credentials from storage.

  If nothing has been stored, or if the stored credentials are invalid,
  the OAuth2 flow is completed to obtain the new credentials.

  Returns:
  Credentials, the obtained credential.
  """
  home_dir = os.path.expanduser('~')
  credential_dir = os.path.join(home_dir, '.credentials')
  if not os.path.exists(credential_dir):
    os.makedirs(credential_dir)
  credential_path = os.path.join(credential_dir,
                                        'sheets.googleapis.com-python-quickstart.json')

  store = Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    if flags:
      credentials = tools.run_flow(flow, store, flags)
    else: # Needed only for compatibility with Python 2.6
      credentials = tools.run(flow, store)
      print('Storing credentials to ' + credential_path)
  return credentials

def main():
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
  service = discovery.build('sheets', 'v4', http=http,
                        discoveryServiceUrl=discoveryUrl)

  spreadsheetId = '1NQjPVqU991QtFjPAOT1tCV1DwSYT-mGnMihW6UA0rz8'
  rangeName = 'GPL570!D:R'
  result = service.spreadsheets().values().get(
                        spreadsheetId=spreadsheetId, range=rangeName).execute()
  
  values = result.get('values', [])

  surv_file = open("GPL570-survival.txt", 'w')

  if not values:
    print('No data found.')
  else:
    for row in values:
      "column"
      for i in xrange(len(row)):
        if i >= 0:
          if row[i] != "N/A":
            surv_file.write(row[i])
        surv_file.write('\t')
      surv_file.write('\n')
  
  surv_file.close()

  #rangeName2 = ['GPL570!C:E', 'GPL570!K1:K']
  #result2 = service.spreadsheets().values().batchGet(
  #                      spreadsheetId=spreadsheetId, ranges=rangeName2).execute()
  
  #values2 = result2.get('values2', []) 

  ih_file = open("GPL570-ih.txt", 'w')
  
  if not values:
    print('No data found.')
  else:
    for row in values:
      for i in xrange(len(row)):
        if i == 0 or i == 1 or i == 9:
          if row[i] != "N/A":
            ih_file.write(row[i])
          ih_file.write('\t')
      ih_file.write('\n')
    ih_file.close()
	
if __name__ == '__main__':
  main()

	
