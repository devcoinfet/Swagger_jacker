import requests 
import sys
import os
import yaml
import json
import bios
import re
import urllib.parse

yaml_endpoint = 'https://example.com/gl.yml'
api_endpoint = 'https://example.com'

auth_token='auth_token'

hed = {'Authorization': 'Bearer ' + auth_token}

def retrieve_swag():
    try:
       yaml_location = swagger_jacker()
       swagger_jacked = bios.read('Yaml_out.yaml')
       total_fuzzable_gets = 0
       api_servers,api_methods = key_play(swagger_jacked)
       print("-"*25)
       print("Api Endpoint Location :"+api_servers)
       print("-"*25)
       print("Api Methods"+"\n")
       print("Method Count: "+str(len(api_methods)))
       print("-"*25)
       for method in api_methods:
           if method:
              matchy = re.findall('{(.+?)}',method)
               #print(method)
              if matchy:
                 #print(method)
                 for matches in matchy:
                     print("Fuzzable Parameters Located")
                     print(matches)
                     total_fuzzable_gets += 1
              else:
                 print("method") 

           else:
             pass
       print("-"*25)
       print("Total Fuzzable Get Parameters :"+str(total_fuzzable_gets))

    except Exception as yamlError:
       print(yamlError)

def swagger_jacker():
    response = requests.get(yaml_endpoint,timeout=3,verify=False)
    output_location = "Yaml_out.yaml"
    #print(response.text)
    if "200" in str(response.status_code):
       print('\n'+"Successfully Grabbed yaml"+'\n')
       yaml_file = open(output_location,"w")
       yaml_file.write(response.text)
       yaml_file.close()
       return response.text
    else:
       print("Yaml Api Definition File Not Located")
     


def key_play(stuff):
    api_servers = ""
    api_paths = []
    for key, value in stuff.items():
        if "servers" in key:
           api_servers += value[0]['url']

        if "paths" in key:
           swagger_paths = json.dumps(value,sort_keys=True, indent=4)
           myJson = json.loads(swagger_paths)
           api_paths = set(myJson.keys())
           for pathsapi in api_paths:
               print(pathsapi)
           for fuzz_items in value.items():
               #print(fuzz_items)
               json_verbiage = json.dumps(fuzz_items[1])
               verbs = json.loads(json_verbiage)
               for verb in verbs.items():
                   print("Method Name: "+fuzz_items[0])
                   print("Method Verb: "+verb[0])
                   if "get" in verb[0]:
                      if len(fuzz_items[0]) == 5:
                          get_params = []
                          for params in verb[1]['parameters']:
                              print(verb[1]['parameters'])
                              for params2 in params.items():
                                  
                                  try:
                                     if "query"   in params2[1]:
                                        continue
                                     if "Unique"   in params2[1]:
                                        continue
                                     
                                     if "type"   in params2[1]:
                                        continue
                                     
                                     if "companyHeaderParam" in str(params2[1]):
                                        continue

                                     else:
                                         if "#/components/parameters/" in str(params2[1]): 
                                             newparam = params2[1].split('/')
                                             clean_param = newparam[-1].replace('Param','')
                                             #print(clean_param)
                                             get_params.append(clean_param)
                                         else:
                                             #print(fuzz_items[0]+":"+str(params2[1]))
                                             get_params.append(params2[1])
                                  except Exception as shit:
                                        print(shit)
                                        pass      
                              print(str(len(get_params))) 
                                
                              '''
                              real_url = ""
                              for itemsin in  get_params:
                                  if itemsin != get_params[-1]:
                                     real_url += itemsin+"=&"
                                  else:
                                     real_url += itemsin+"=&"
                              print(real_url) 
                              '''                      
               
        else:
           pass
           #print(key)

    return api_servers,api_paths



def main():

    retrieve_swag()


main()
