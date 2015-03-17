# run this code to write google doc

import intercom_api
import intercom
from intercom import Intercom
from datetime import datetime
from intercom import User
import salesforce_api
import beatbox
import gspread
 
def format_per(float_number):
    return '{:.2f}'.format(float_number)+'%'

def format_datetime(datetime_obj):
    return str(datetime_obj)[:str(datetime_obj).rfind(':')+3]

def open_or_create_new_file(filename):
    import gspread
    import gdata.docs.client
    
    email = 'tiger@viewsy.com'
    password = 'Qq18666372882'
    gc = gspread.login(email, password)
        
    #Tries to Open Spreadsheet. If doesn't exist, creates new
    try:
            spr = gc.open(filename)
    except:
            gd_client = gdata.docs.client.DocsClient()
            source = 'Monthly Spreadsheet'
            gd_client.ClientLogin(email, password, source)
            document = gdata.docs.data.Resource(type='spreadsheet', title=filename)
            document = gd_client.CreateResource(document)
            print 'Created Spreadsheet: '+filename
            spr = gc.open(filename)
            pass
        
    return spr
    
    #!/usr/bin/python
    
def retrieve_all_files(service):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  result = []
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      files = service.files().list(**param).execute()

      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return result
  
def share_to_email(email_adress,file_title):
    
    import httplib2
    import pprint
    
    from apiclient.discovery import build
    from apiclient.http import MediaFileUpload
    from oauth2client.client import OAuth2WebServerFlow
    from apiclient import errors

    def get_file_id_by_title(file_title,drive_service):
        
        all_files = retrieve_all_files(drive_service)
        for i in all_files:
            if i['title'] == file_title:
                return i['id']
                
        return 'Unknown Name'
    
    # Copy your credentials from the console
    CLIENT_ID = '939580449229-cravutimuekt3po888glao95aa7fck53.apps.googleusercontent.com'
    CLIENT_SECRET = '8ouu5xZGzHK402L6I-X3w62A'
    
    # Check https://developers.google.com/drive/scopes for all available scopes
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
    
    # Redirect URI for installed apps
    REDIRECT_URI = 'https://www.example.com/oauth2callback'
    
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                            redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    
    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    drive_service = build('drive', 'v2', http=http)
    
    """Insert a new permission.

    Args:
        service: Drive API service instance.
        file_id: ID of the file to insert permission for.
        value: User or group e-mail address, domain name or None for 'default'
            type.
        perm_type: The value 'user', 'group', 'domain' or 'default'.
        role: The value 'owner', 'writer' or 'reader'.
    Returns:
        The inserted permission if successful, None otherwise.
    """
    new_permission = {
        'value': email_adress,
        'type': 'user',
        'role': 'writer'
    }
    try:
        return drive_service.permissions().insert(
            fileId=get_file_id_by_title(file_title,drive_service), body=new_permission).execute()
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
    return None
    
if __name__ == '__main__':
    ############################# intercom #############################
    # Authorization
    Intercom.app_id = 'yb8sxeop'
    Intercom.api_key = '7ab67c8504401831c5898148de01091b09af936f'
    
    # get the metric
    intercom_metrics = intercom_api.per_active_user(intercom.User.all(),30)
    print 'finish getting data from intercom'
    
    ############################# salesforce #############################
    svc = beatbox.PythonClient()
    svc.login('tiger@viewsy.com', 'Qq18666372882s7jF6atSena3eAIQo7jue6Q4T')
    salesforce_metrics = salesforce_api.get_metrics(svc)
    print 'finish getting data from salesforce'
    
    ############################# Write to google doc #############################
    gc = gspread.login('tiger@viewsy.com', 'Qq18666372882')
    
    file_title = "testing_metrics_1"
    wks = open_or_create_new_file(file_title)
    
    wks.add_worksheet('p/m fit',10,10)
    wks.add_worksheet('sales',10,10)
        
    wks_pmfit = wks.worksheets()[0]
    
    wks_pmfit.update_acell('A1','% of convertion:')
    wks_pmfit.update_acell('B1',format_per(salesforce_metrics[1]['pro_count']['pro_1_8']))
    
    wks_pmfit.update_acell('A2','Average time of convertion:')
    wks_pmfit.update_acell('B2',format_datetime(salesforce_metrics[1]['time_count']['ave_time_1_8']))
    
    wks_pmfit.update_acell('A4','How much do \'active user\' use our app?')
    wks_pmfit.update_acell('B4',format_per(intercom_metrics))
    
    wks_pmfit.update_acell('A5','How long?')
    wks_pmfit.update_acell('B5','No data')
    
    wks_sales = wks.worksheets()[1]

    # setting the framework
    wks_sales.update_acell('B1','count')
    wks_sales.update_acell('C1','Proportion to Qualified Stage')
    wks_sales.update_acell('D1','average time of progressing to next stage')
    
    wks_sales.update_acell('A3','Initial Meeting')
    wks_sales.update_acell('A5','Qualified')
    wks_sales.update_acell('A7','Final Proposal')
    wks_sales.update_acell('A9','Won')
    
    # set the count value
    wks_sales.update_acell('B3','?')
    wks_sales.update_acell('B5',salesforce_metrics[0]['stage_count']['stage_1_count'])
    wks_sales.update_acell('B7',salesforce_metrics[0]['stage_count']['stage_5_count'])
    wks_sales.update_acell('B9',salesforce_metrics[0]['stage_count']['stage_8_count'])
    
    # set the % value
    wks_sales.update_acell('C4','?')
    wks_sales.update_acell('C6',format_per(salesforce_metrics[0]['pro_count']['pro_1_5']))
    wks_sales.update_acell('C8',format_per(salesforce_metrics[0]['pro_count']['pro_1_8']))
    
    # set the average time
    wks_sales.update_acell('D4','?')
    wks_sales.update_acell('D6',format_datetime(salesforce_metrics[0]['time_count']['ave_time_1_5']))
    wks_sales.update_acell('D8',format_datetime(salesforce_metrics[0]['time_count']['ave_time_5_8']))
    print 'finish writing google spreadsheet'

    wks = gc.open(file_title)
    gc.del_worksheet(wks.worksheet('Sheet1'))
    
    ############################# Share to email #############################
    #share_to_email('odera@viewsy.com',file_title)
    #print 'finish sharing'