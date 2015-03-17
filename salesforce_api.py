import datetime

def list_of_oppurtunities(oppurtunites_list):
        
    # store the data
    data_stage_date = []
    for each_data in oppurtunites_list:
        try:
            data_stage_date.append([int(each_data['StageName'][0]),each_data['CreatedDate']])
        except ValueError:
            pass
    data_stage_date = sorted(data_stage_date, key=lambda x:x[1])
    
    # deleting the repeated stages
    new_data_stage_date = []
    all_stages = sorted(list(set([i[0] for i in data_stage_date])))
    for each_stage_value in all_stages:
        for data in data_stage_date:
            if each_stage_value == data[0]:
                new_data_stage_date.append(data)
                break
                
    new_data_stage_date = sorted(new_data_stage_date,key=lambda x:x[0],reverse=True)
    
    return new_data_stage_date # return stage and time

def calculate_time_metrics(stage_and_time):
    stage_and_time = sorted(stage_and_time,key=lambda x:x[0])
    stage_and_time = [{'stage':i[0],'time':i[1]} for i in stage_and_time]
    
    metric_stage_list = [{'stage':1,'time':None},{'stage':5,'time':None},{'stage':8,'time':None}]
    
    for each_data in stage_and_time:
        for metric_stage in metric_stage_list:
            if metric_stage['time'] == None:
                if each_data['stage'] >= metric_stage['stage'] and each_data['stage']!=9:# stage 9 is lose
                    metric_stage['time'] = each_data['time'] 
    return metric_stage_list

def average_time(timedelta_list):# function is for calculating an average time from a timedelta list
    
    seconds_all = []
    for i in timedelta_list:
        if i.total_seconds() >= 0:
            seconds_all.append(i.total_seconds())
    average_seconds = sum(seconds_all)/len(seconds_all)
    return datetime.timedelta(seconds=average_seconds)

def metrics_calculator(metrics_stage_time_all):
    
    result = {'stage_count':{'stage_1_count':0,'stage_5_count':0,'stage_8_count':0},
              'pro_count':{'pro_1_5':0,'pro_1_8':0},
              'time_count':{'ave_time_1_5':0,'ave_time_5_8':0}
              }
    
    ave_time_1_5_list = []
    ave_time_5_8_list = []
    
    for metrics_stage_time in metrics_stage_time_all:
        
        if metrics_stage_time[0]['time'] != None:
            result['stage_count']['stage_1_count'] += 1
            
        if metrics_stage_time[1]['time'] != None:
            result['stage_count']['stage_5_count'] += 1
            ave_time_1_5_list.append(metrics_stage_time[1]['time']-metrics_stage_time[0]['time'])
            
        if metrics_stage_time[2]['time'] != None:
            result['stage_count']['stage_8_count'] += 1
            ave_time_5_8_list.append(metrics_stage_time[2]['time']-metrics_stage_time[1]['time'])
    
    # calculate the probabilities
    result['pro_count']['pro_1_5'] = float(result['stage_count']['stage_5_count'])*100/result['stage_count']['stage_1_count']
    result['pro_count']['pro_1_8'] = float(result['stage_count']['stage_8_count'])*100/result['stage_count']['stage_1_count']
    
    # calculate the average time
    result['time_count']['ave_time_1_5'] = average_time(ave_time_1_5_list)
    result['time_count']['ave_time_5_8'] = average_time(ave_time_5_8_list)
    
    result_pm_fit = {
              'pro_count':{'pro_1_8':result['pro_count']['pro_1_8']},
              'time_count':{'ave_time_1_8':result['time_count']['ave_time_1_5']+result['time_count']['ave_time_5_8']}
              }
    
    return [result,result_pm_fit]

def get_metrics(svc):
    
    qr = svc.query("select CreatedDate,OpportunityId,StageName from OpportunityHistory where CreatedDate>2014-12-01T00:00:00Z")
        
    list_all_id = []
    for i in qr:
        list_all_id.append(i['OpportunityId'])
    
    oppurtunites = []
    for opp_id in list(set(list_all_id)):# unique oppur id
        oppurtunites.append([])
        for data in qr:
            if data['OpportunityId'] == opp_id:
                oppurtunites[-1].append(data)# append the same changes for the same opportunities
    
    metrics_stage_time_all = []
    for i in oppurtunites:
        stage_and_time = list_of_oppurtunities(i)
        metrics_stage_time_all.append(calculate_time_metrics(stage_and_time))
        
    return metrics_calculator(metrics_stage_time_all)
    
if __name__ == '__main__':
    
    import beatbox
    svc = beatbox.PythonClient()
    svc.login('tiger@viewsy.com', 'Qq18666372882s7jF6atSena3eAIQo7jue6Q4T')
    print get_metrics(svc)