import requests
import urllib
import json
from cleantext import clean
import timeit
import operator
import pandas as pd

#Function to call BERN API 
def query_raw(text, url="BERN API URL"):
    body_data = {"param": json.dumps({"text": text})}

    return requests.post(url, data=body_data).json()

time_dict = {}
#Fetch 5 documents from the solr server
connection = urllib.request.urlopen('http://solr-server-address:port/solr/core_name/select?fl=id,sem_title,detailed_*,brief_*,drug_*,eligibility_*,sem_record_type,&fq=sem_record_type:ClinicalTrials.gov\%20Record&q=*:*&rows=5&wt=json')
response = json.load(connection)

for document in response['response']['docs']:
    start_time = timeit.default_timer()
    trial_id = document['id']
    output_dict = {}
    denotations_array = []
    denotation_dict ={}
    
    with open(str(trial_id)+'.json', 'w') as file:
     
        output_dict['id'] = trial_id

        #Check for the presence of sem_title field in the document
        if('sem_title' in document and len(document['sem_title'])!=0):
            sem_title = clean(document['sem_title'],no_line_breaks=True)

        else:
            sem_title = 'Not Available'

        output_dict['sem_title'] = sem_title

        #Check for the presence of brief_summary field in the document
        if('brief_summary' in document and len(document['brief_summary'])!=0):
            #Cleaning text for breaks and string typecasting
            brief_summary = str(clean(document['brief_summary'],no_line_breaks=True))

            #Fetching denotations for the text
            brief_summary_entities = query_raw(brief_summary)
            
            #Iterating over the denotations to extract the object text             
            for denotation in brief_summary_entities['denotations']:
                
                denotation_dict['id'] = denotation['id']
                denotation_dict['span'] = denotation['span']
                denotation_dict['obj_text'] = brief_summary[denotation['span']['begin']:denotation['span']['end']]
                denotation_dict['obj'] = denotation['obj']
                denotations_array.append(denotation_dict)

                denotation_dict ={}

            brief_summary_entities = denotations_array.copy()

        else:
            brief_summary = 'Not Available'
            brief_summary_entities = 'Not Available'


        output_dict['brief_summary'] = brief_summary
        output_dict['brief_summary_entities'] = brief_summary_entities

        denotations_array = []

        if('detailed_description' in document and len(document['detailed_description'])!=0):
            detailed_description = clean(document['detailed_description'],no_line_breaks=True)
            detailed_description_entities = query_raw(detailed_description)

            #Iterating over the denotations to extract the object text
            for denotation in detailed_description_entities['denotations']:
                denotation_dict['id'] = denotation['id']
                denotation_dict['span'] = denotation['span']
                denotation_dict['obj_text'] = detailed_description[denotation['span']['begin']:denotation['span']['end']]
                denotation_dict['obj'] = denotation['obj']
                denotations_array.append(denotation_dict)

                denotation_dict ={}

            detailed_description_entities = denotations_array.copy()

            output_dict['detailed_description'] = detailed_description
            output_dict['detailed_description_entities'] = detailed_description_entities

        else:
            detailed_description = 'Not Available'
            detailed_description_entities = 'Not Available'

        output_dict['detailed_description'] = detailed_description
        output_dict['detailed_description_entities'] = detailed_description_entities

        denotations_array = []
        #Check for the presence of eligibility_criteria field in the document
        if('eligibility_criteria' in document and len(document['eligibility_criteria'])!=0):
            
            eligibility_criteria = clean(document['eligibility_criteria'],no_line_breaks=True)
            eligibility_criteria_entities = query_raw(eligibility_criteria)
            
            for denotation in eligibility_criteria_entities['denotations']:
                denotation_dict['id'] = denotation['id']
                denotation_dict['span'] = denotation['span']
                denotation_dict['obj_text'] = eligibility_criteria[denotation['span']['begin']:denotation['span']['end']]
                denotation_dict['obj'] = denotation['obj']
                denotations_array.append(denotation_dict)

                denotation_dict ={}

            eligibility_criteria_entities = denotations_array.copy()

            output_dict['detailed_description'] = eligibility_criteria
            output_dict['detailed_description_entities'] = eligibility_criteria_entities

            denotations_array = []

        else:
            eligibility_criteria = 'Not Available'
            eligibility_criteria_entities = 'Not Available'

        output_dict['eligibility_criteria'] = eligibility_criteria
        output_dict['eligibility_criteria_entities'] = eligibility_criteria_entities

        denotations_array = []
        denotations_array = []
         
        json.dump(output_dict, file)
    elapsed = timeit.default_timer() - start_time
    time_dict.update({str(trial_id) : elapsed})
    print('Doc ID: ', str(trial_id), '  Time elapsed:', str(elapsed))

max_time_doc_id = max(time_dict, key=time_dict.get)
print('Maximum time taken by doc: ',max_time_doc_id,' Time elapsed:'+str(time_dict.get(max_time_doc_id)))

print('Average time per doc: ', str(pd.Series([*time_dict.values()]).mean()))

min_time_doc_id = min(time_dict, key=time_dict.get)
print('Minimum time taken by doc: ',min_time_doc_id,' Time elapsed:'+str(time_dict.get(min_time_doc_id)))

df = pd.DataFrame.from_dict(time_dict, orient='index')
df.to_csv('time_stats.csv', '\t', header=False, index=True)