def is_active_user(user,dates_determine_active=30):
    
    '''
    1. input user's last_impression_at timestamp if user log in with in 30 days then this user is active
    2. if user had logged once in X days(dates_determine_active) then this user is defined to be active. 
    '''
    
    last_impression_at = user['last_impression_at']
    
    if last_impression_at == None:
        print 'No last_impression_at'
        return False
    
    import datetime 
    date_now = datetime.datetime.now().date()
    active_days = date_now - datetime.timedelta(seconds=dates_determine_active*24*60*60)
    
    date_from_timestamp = datetime.datetime.fromtimestamp(float(last_impression_at)).date()
    if active_days <= date_from_timestamp <= date_now:
        return True
    else:
        return False
    
def is_viewsy_user(user):
    '''
    The idea of this function is to ignore the user with viewsy.com email, since they are not actual user. 
    '''
    fake_account_list = ['dkjfh@jhdf.com','jdfkh@jfh.com','fox@itsfox.eu','dfkj@kjdfk.com',
                     'ghost.miha@gmail.com','test@test1.com','jasper.diegostory@gmail.com',
                     'jan.simek@itsfox.eu','fox@itsfox.eu','jasper.diegostory@gmail.com','jasper.diegostory@gmail.com',
                     'fox.simek@gmail.com']
    
    email_address = user['email']
    
    if '@viewsy.com' in email_address or email_address in fake_account_list:
        return True
    else:
        return False

def get_session_counts(user_all,does_ignore_viewsy_user=True):
    '''
    Get the number of session counts from intercom
    '''    
    counts = []
    for user in user_all:
        if does_ignore_viewsy_user:
            if is_active_user(user['last_impression_at']) and not is_viewsy_user(user['email']):
                counts.append({'user_id':user['user_id'],'session_count':user['session_count']})
        else:
            if is_active_user(user['last_impression_at']):
                counts.append({'user_id':user['user_id'],'session_count':user['session_count']})
    return counts

def get_user_all(user_all,does_ignore_viewsy_user=True):
    '''
    Get the number of session counts for all users from intercom
    '''
    counts = []
    for user in user_all:
        if does_ignore_viewsy_user:
            if not is_viewsy_user(user):
                counts.append(user)
        else:
            counts.append(user)
    return counts
    
def per_active_user(user_all,dates_deter_active):
    any_user_all = get_user_all(user_all,does_ignore_viewsy_user=True)
    active_user_all = []
    for user in any_user_all:
        if is_active_user(user,dates_determine_active=dates_deter_active):
            active_user_all.append(user)
    return float(len(active_user_all))*100/len(any_user_all)
    
if __name__ == '__main__':
                     
    from intercom import Intercom
    from intercom import User
    
    # Authorization
    Intercom.app_id = 'yb8sxeop'
    Intercom.api_key = '7ab67c8504401831c5898148de01091b09af936f'
    
    # get the metric    
    print 'testing',per_active_user(User.all(),30)