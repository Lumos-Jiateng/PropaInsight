
# preprocess the data for appeals 
import pandas as pd
import json
from collections import Counter

file_path_kitware = '/shared/nas/data/m1/jiateng5/semafor-data/human_annotated_results/kitware/export_72088_project-72088-at-2024-06-13-20-17-3b7f9fc4.json'

file_path_rapidata_context_1 = '/shared/nas/data/m1/jiateng5/semafor-data/human_annotated_results/rapidata/desciption_matches_context_first_99.json'

file_path_rapidata_feelings_1 = '/shared/nas/data/m1/jiateng5/semafor-data/human_annotated_results/rapidata/desciption_matches_feelings_first_99.json'

file_path_rapidata_context_2 = '/shared/nas/data/m1/jiateng5/semafor-data/human_annotated_results/rapidata/description_matches_context_100_1000.json'

file_path_rapidata_feelings_2 = '/shared/nas/data/m1/jiateng5/semafor-data/human_annotated_results/rapidata/description_matches_feelings_100_1000.json'

file_path_kitware_intent = '/shared/nas/data/m1/jiateng5/semafor-data/human_annotated_results/kitware/export_72090_project-72090-at-2024-06-13-20-26-05c64f5b.json'

with open(file_path_kitware,'r') as f: 
    kitware_data = json.load(f)

with open(file_path_kitware_intent,'r') as ff: 
    kitware_intent_data = json.load(ff)

with open(file_path_rapidata_context_1,'r') as f1:
    rapidata_context_1 = json.load(f1)

with open(file_path_rapidata_context_2,'r') as f2:
    rapidata_context_2 = json.load(f2)

with open(file_path_rapidata_feelings_1,'r') as g1:
    rapidata_feelings_1 = json.load(g1)
    
with open(file_path_rapidata_feelings_2,'r') as g2:
    rapidata_feelings_2 = json.load(g2)

rapiddata_context = rapidata_context_1['results']['data']+rapidata_context_2['results']['data']

rapiddata_feelings = rapidata_feelings_1['results']['data']+rapidata_feelings_2['results']['data']

# Get kitware annotated datalist
#import ipdb;ipdb.set_trace()
def count_elements(data):
    # Count the frequency of each element in the list
    counter = Counter(data)
    # Convert the counter object to a list of tuples (element, frequency)
    return list(counter.items())

article_id_list = []
for i in range(len(kitware_data)):
    kitware_data_piece = kitware_data[i]
    article_id = kitware_data_piece['data']['data_id']
    article_id_list.append(article_id)

# process the article id list to confirm the number of annotations.
distribution_list = count_elements(article_id_list)

#import ipdb;ipdb.set_trace()

csv_path = '/mnt/data/Data_For_Annotation.csv'
data = pd.read_csv('/shared/nas/data/m1/jiateng5/semafor-data/Rapidata/Data_For_Annotation.csv')
data_list = data.to_dict(orient='records')

id_list = []
for i in range(len(data_list)): 
    id_list.append(data_list[i]['data_id'])

distribution_list_1 = count_elements(id_list)

with open('/shared/nas/data/m1/jiateng5/semafor-data/Data/ptc_all.json','r') as ptc:
    ptc_original_data = json.load(ptc) 

target_path = '/shared/nas/data/m1/jiateng5/semafor-data/Data/ptc_human_annotated.json'

# Get the full annotation data list 
ptc_data_human_annotated = []
#import ipdb;ipdb.set_trace()

def find_annotation_list(sentence,appeal,kitware_data):
    annotation_list = []
    flag = 0
    for i in range(len(kitware_data)):
        kitware_annotation_data = kitware_data[i]
        if kitware_annotation_data['data']['Target_Sentence'] == sentence and kitware_annotation_data['data']['Descriptive_Sentence'][22:] == appeal:
            annotation_list.append(kitware_annotation_data) 
            flag = 1
    if flag == 1:
        print(f'find annotated data piece of length {len(annotation_list)}') 
    return annotation_list 

def find_annotation_list_intent(intent,kitware_data):
    annotation_list = []
    flag = 0
    for i in range(len(kitware_data)):
        kitware_annotation_data = kitware_data[i]
        if kitware_annotation_data['data']['Descriptive_Sentence'][22:] == intent:
            annotation_list.append(kitware_annotation_data) 
            flag = 1
    if flag == 1:
        print(f'find annotated data piece of length {len(annotation_list)}') 
    return annotation_list 

for j in range(len(ptc_original_data)):
    # in terms of articles, define the annotation list. focus on appeals 
    kitware_annotation_list = []
    original_data = ptc_original_data[j]
    id = ptc_original_data[j]['id']
    current_appeal_number = len(ptc_original_data[j]['span_tactic_list'])
    temp_dict = ptc_original_data[j]
    annotated_flag = 0
    for k in range(current_appeal_number):
        appeal = ptc_original_data[j]['span_tactic_list'][k]['appeal']
        sentence = ptc_original_data[j]['span_tactic_list'][k]['sentence']
        kitware_annotation_list = find_annotation_list(sentence,appeal,kitware_data)
        #import ipdb;ipdb.set_trace()
        if len(kitware_annotation_list)>=1:
            annotated_flag = 1
            if len(kitware_annotation_list)>1:
                print('multiple annotations')    
        if len(kitware_annotation_list)==0:
            print('not_annotated')
            continue
        kitware_annotation_list = [kitware_annotation_list[0]] # select the first available annotation 
        for m in range(len(kitware_annotation_list)):
            annotations = kitware_annotation_list[m]['annotations'][0]['result']
            for result in annotations:
                if result['type'] == 'choices':
                    temp_dict['span_tactic_list'][k]['judgement_kitware'] = result['value']['choices'][0]
                if result['type'] == 'textarea':
                    #import ipdb;ipdb.set_trace()
                    temp_dict['span_tactic_list'][k]['remark_kitware'] = result['value']['text'][0]
                #temp_dict['span_tactic_list'][k]['remark_kitware'] = 'Empty'
            #if len(annotations) == 1: 
    # annotation for intents
    current_intent_number =  len(ptc_original_data[j]['intents'])
    temp_dict['intents'] = [{'intents': intent} for intent in temp_dict['intents']]
    temp_dict['intents'][0]['judgement_kitware'] = "Yes, the intent is correct."
    for t in range(current_intent_number):
        intent = ptc_original_data[j]['intents'][t]['intents']
        #import ipdb;ipdb.set_trace()
        intent_annotation_list = find_annotation_list_intent(intent,kitware_intent_data)
        if len(intent_annotation_list)>=1:
            annotated_flag = 1
            if len(intent_annotation_list)>1:
                print('multiple intent annotations')    
        if len(intent_annotation_list)==0:
            print('intent not annotated')
            continue
        intent_annotation_list = [intent_annotation_list[0]]
        for m in range(len(intent_annotation_list)):
            annotations = intent_annotation_list[m]['annotations'][0]['result']
            for result in annotations:
                if result['type'] == 'choices':
                    temp_dict['intents'][t]['judgement_kitware'] = result['value']['choices'][0]
                elif result['type'] == 'textarea':
                    #import ipdb;ipdb.set_trace()
                    temp_dict['intents'][t]['remark_kitware'] = result['value']['text'][0]
    if annotated_flag == 1:
        ptc_data_human_annotated.append(temp_dict) 
'''
for j in range(len(ptc_original_data)):  
    kitware_annotation_list = []
    id = ptc_original_data[j]['id']
    for i in range(len(kitware_data)):
        kitware_data_piece = kitware_data[i]
        article_id = kitware_data_piece['data']['data_id']
        # find the original_article
        if ptc_original_data[j]['id'] == article_id:
            kitware_annotation_list.append(kitware_data_piece)
    if len(kitware_annotation_list)!=0:
        print(f'generating annotation for article {id}')
        if len(kitware_annotation_list) == len(ptc_original_data[j]['span_tactic_list']):
            print(f'all appeals annotated with kitware in {id}')
            temp_dict = ptc_original_data[j]
            for k in range(len(kitware_annotation_list)):
                #import ipdb;ipdb.set_trace()
                if len(kitware_annotation_list[k]['annotations'][0]['result']) == 0:
                    continue
                if len(kitware_annotation_list[k]['annotations'][0]['result']) == 1 and 'choices' in kitware_annotation_list[k]['annotations'][0]['result'][0]['value'].keys():
                    try: 
                        temp_dict['span_tactic_list'][k]['judgement_kitware'] = kitware_annotation_list[k]['annotations'][0]['result'][0]['value']['choices'][0]
                        temp_dict['span_tactic_list'][k]['remark_kitware'] = 'Empty'
                    except:
                        import ipdb;ipdb.set_trace()  
                        continue 
                else: 
                    if 'choices' in kitware_annotation_list[k]['annotations'][0]['result'][0]['value'].keys():
                        temp_dict['span_tactic_list'][k]['judgement_kitware'] = kitware_annotation_list[k]['annotations'][0]['result'][0]['value']['choices'][0]
                        temp_dict['span_tactic_list'][k]['remark_kitware'] = kitware_annotation_list[k]['annotations'][0]['result'][1]['value']['text'][0]
                    else: 
                        temp_dict['span_tactic_list'][k]['remark_kitware'] = kitware_annotation_list[k]['annotations'][0]['result'][0]['value']['text'][0]
            ptc_data_human_annotated.append(temp_dict)        
        elif len(kitware_annotation_list) == 2*len(ptc_original_data[j]['span_tactic_list']):
            print(f'repeated annotation, compute agreement rate at the same time')
            temp = kitware_annotation_list
            print('annotating sample_1')
            #import ipdb;ipdb.set_trace()
            kitware_annotation_list = temp[:int(len(temp)/2-1)]
            for k in range(len(kitware_annotation_list)):
                #import ipdb;ipdb.set_trace()
                if len(kitware_annotation_list[k]['annotations'][0]['result']) == 0:
                    continue
                if len(kitware_annotation_list[k]['annotations'][0]['result']) == 1 and 'choices' in kitware_annotation_list[k]['annotations'][0]['result'][0]['value'].keys():
                    try: 
                        temp_dict['span_tactic_list'][k]['judgement_kitware'] = kitware_annotation_list[k]['annotations'][0]['result'][0]['value']['choices'][0]
                        temp_dict['span_tactic_list'][k]['remark_kitware'] = 'Empty'
                    except:
                        import ipdb;ipdb.set_trace()  
                        continue 
                else: 
                    if 'choices' in kitware_annotation_list[k]['annotations'][0]['result'][0]['value'].keys():
                        temp_dict['span_tactic_list'][k]['judgement_kitware'] = kitware_annotation_list[k]['annotations'][0]['result'][0]['value']['choices'][0]
                        temp_dict['span_tactic_list'][k]['remark_kitware'] = kitware_annotation_list[k]['annotations'][0]['result'][1]['value']['text'][0]
                    else: 
                        temp_dict['span_tactic_list'][k]['remark_kitware'] = kitware_annotation_list[k]['annotations'][0]['result'][0]['value']['text'][0]
            ptc_data_human_annotated.append(temp_dict)    
        else:
            print(len(kitware_annotation_list))
            print(len(ptc_original_data[j]['span_tactic_list']))
            print('not annotated completely, skip')
            continue
'''        
with open(target_path,'w') as t:
    json.dump(ptc_data_human_annotated,t)    
    
# Do calculations here: 

#annotated_number = 0
#for data in ptc_data_annotated 
    
