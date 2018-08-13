
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
from itertools import chain
from datetime import datetime
import re
from urllib.parse import urlparse, urlsplit
import os
import random
import time 
from scipy.stats import uniform, levy
import numpy as np
import calendar
import numpy as np 
import platform


# In[2]:


sys = platform.system()
print(sys)


# In[3]:


if sys == 'Windows':
    current_folder =  str(os.getcwd()+'\\')
    path_results = current_folder + 'results_medium_standard\\'
else:
    current_folder =  str(os.getcwd()+'/')
    path_results = current_folder + 'results_medium_standard/'
print(current_folder)
print(path_results)
print(' ')
print(' ')


# In[4]:


site_to_search = 'medium.com'
loc = '+loc%3Abr'
cc = '+cc%3Apt-BR'


# In[5]:


# keywords_list = ['animais', 'artes', 'atualidades', 'bebes', 'beleza', 'ciencia', 'cinema',\
#                  'cultura',\
#                  'decoracao', 'design', 'economia',\
#                  'educacao', 'emprego', 'entretenimento', 'espiritualidade', 'esportes', 'estilo+de+vida',\
#                  'familia', 'financas', 'fitness', 'futebol', 'gastronomia', 'humor',\
#                  'infantil', 'internet', 'jornal', 'jornalismo', 'literatura', 'meio+ambiente', 'moda',\
#                  'musica', 'natureza', 'negocios',  'noticias', 'politica', 'saude', 'tecnologia', 'televisao', \
#                  'tv', 'variedades', 'viagens']

keywords_list = ['animais']


# In[6]:


# a function that generates a random number to be used as the sleep time. This
# uses a mixture of normal and levy distribution in order to bypass the server firewalls.
def random_sleep_time():
    dt = 0
    while dt > 30 or dt < 2 :
        dt = 1.5*uniform.rvs(size=1)[0]*levy.rvs(size=1)[0]
    return dt    
   


# In[7]:


# A function that corrects the end day of a given month. For example, 28/02 or 29/02?
def end_day_corrector(day, month, year):

    try:
       
        date_list = [str(month), str(day), str(year)]
        final_date = '-'.join(date_list)        
        
        d = datetime.strptime(final_date, '%m-%d-%Y')
        
        
    except ValueError:
        #print('wrong final day of the month!!!')
        #day = day -1
        final_date = end_day_corrector(day-1, month, year)
        
        
    
    return final_date


# In[8]:


def unix_date_day(day, month, year):
    
    input_date = end_day_corrector(day, month, year)
    
    d = datetime.strptime(input_date, '%m-%d-%Y')
    
    unixtime = calendar.timegm(d.utctimetuple())
    unixtime_day = unixtime/60/60/24
    
    return unixtime_day
    


# In[9]:


unix_time_dict = {}
interval_complete_list = []

month_year_list = []
k= 0
for year in range(2007, 2008):
    
    for month in range(1, 13):
        
  
        start_date = unix_date_day(1, month, year)

        end_date = unix_date_day(31, month, year)



        interval_date_list = [start_date, end_date]

        print(k, ' ',  year, ' ', month, ' ', interval_date_list)
        k += 1
       
        interval_complete_list.append(interval_date_list)
        month_year_list.append(str(month) + '_' + str(year))
        
        
        if year == 2018 and month >= 5:
            break
    
print(' ')
print(' ')


# In[10]:


if os.path.exists(str(path_results + 'idx_medium_forward.dat')) == True:
    f = open(path_results + 'idx_medium_forward.dat', 'r' )
    start = f.readlines()[0]
    idx_start = int(start)
    f.close()
    
else:
    idx_start = 0
    
print('idx_start: ', idx_start)


# In[11]:


years_list = range(2007, 2008, 1)


# In[ ]:


time_list = []
global_start_time = time.time()
requisicao = 0

        
for j in range(idx_start, len(keywords_list)):
    
               
    start_time = time.time()
    search_term = keywords_list[j]
    k = 1

    for year in years_list:
        
        for k in range(9, 29, 10):


            try:

                start = str(k)
                
                
                url_search_1 = 'https://www.bing.com/search?q='
                url_search_2 = search_term + '+site%3A' + site_to_search + cc            
                url_search_4 = '&qs=HS&sc=3-0&cvid=E2EAF9B741E34472B3DF8F49392E96AF&sp=1&first=' + str(k) + '&FORM=PERE1' 
               
                #bing
               
            

                # gathering the pieces of url:
                #full_url = url_search_1 + url_search_2 + url_search_3 + url_search_4
                full_url = url_search_1 + url_search_2 + url_search_4
                print(full_url)

                sites_list = [full_url]


                # let's use a time sleep function before the requests in order to avoid blocks from Bing server:
                dt = random_sleep_time()
                print(search_term, ' ', year, 'step: ', k)
                print('sleep time: ', dt/10)
                time.sleep(dt/10)
                
                print(' ')
                print(' ')

                one_page = requests.get(str(sites_list[0]))
                print(one_page)
                requisicao += 1
                
                if one_page.status_code != 200:       
                    print("ERRO")

                    filename = 'failed_keywords_google.dat'
                    #verification folder exists
                    if os.path.exists(str(path_results)) == True:                    
    #                     print('The folder exists')

                        if os.path.exists(str(path_results + filename)) == True:
                            f = open(path_results + filename, 'a' )
                        else:
                            f = open(path_results + filename, 'w' )
                        f.write(search_term + ',' + str(j) + ',' + str(k) + "\n")
                        f.close()  

                    else:

                        print('Folder does not exist')
                        #make folder if not exists
                        os.mkdir('results_google_standard')

                        f = open(path_results + filename, 'w' )
                        f.write(search_term + ',' + str(j) + ',' + str(k) + "\n")
                        f.close()
                        print('Folder created')
                    continue

                    sleep_block = 600
                    print(' ')
                    print('Blocked by Bing! Now sleeping for {} seconds'.format(sleep_block))
                    print(' ')
                    time.sleep(sleep_block)
                    continue


                pages_set = []
                pages_set.append(one_page)


        # Getting the html content of all pages listed above:
                soup_list = []
                for ij in range(0,len(pages_set)):
                    try:
                        soup_list.append(BeautifulSoup(pages_set[ij].content, 'html.parser'))
                    except:
                        # repeat the last item in order to avoid problems.. This item is
                        # elimanted in the last step to avoid redundance        
                        soup_list.append(BeautifulSoup(pages_set[ij-1].content.decode('utf-8'), 'html.parser'))
                        continue

                links=[]
                for jj in range(0,len(pages_set)):
                    for link in soup_list[jj].find_all('a'):
                        links.append(link.get('href'))           



                linkss = []
                for ii in range(0,len(links)):
                    try:
                        linkss.append(str(links[ii]))
                        #print str(links[ii])
                    except:
                        continue      



                #print linkss
                #print ' '
                #print ' '                 



                archive = []
                for item in linkss:
                    if 'medium.com' in item and '.files.' not in item and '.bing.com' not in item:
                        result = re.search('https://medium.com/@(.*)/', item)
                        if result:
                            archive.append(result.group(0))



                print(archive)

                archive_filtered_zero = []
                for k in range(0,len(archive)):
                    split_url = urlsplit(archive[k])
                    final_url = split_url[0] + '://' + split_url[1] + split_url[2][0:-1]
                    archive_filtered_zero.append(final_url)


                archive_filtered_one = list(set(archive_filtered_zero))
                print(archive_filtered_one)
                print('collected sources: ', len(archive_filtered_one))



                new_sources_list = list(set(archive_filtered_one) )    


                #### writing the found sources to a file whose name is linked to the associated keyword.

                #creating or loading the file to append the new sources found:
                keyword_filename = 'new_links_medium_' + str(search_term) + '.dat'                
                
                if os.path.exists(str(path_results)) == True:                    
#                     print('The folder exists')
                
                    if os.path.exists(str(path_results + keyword_filename)) == True:
                        f = open(path_results + keyword_filename, 'a' )
                    else:
                        f = open(path_results + keyword_filename, 'w' )

                    for k in range(0, len(new_sources_list)):
                        f.write(new_sources_list[k]+"\n")
                    f.close()
                    
                else:
                    print('Folder does not exist')
                    os.mkdir('results_medium_standard')

                    f = open(path_results + keyword_filename, 'w' )

                    for k in range(0, len(new_sources_list)):
                        f.write(new_sources_list[k]+"\n")
                    f.close()


                # reading the file to eliminate duplicates:
                final_list_keyword = []
                current_folder =  str(os.getcwd()+'/')
                f = open(str(path_results + keyword_filename), 'r')
                for line in f:
                    line = line.strip()
                    final_list_keyword.append(line)
                f.close()    


                # writing the de-duplicated source list to a final file:
                keyword_filename_final = 'new_links_medium_' + str(search_term) + '_filtered.dat'
                final_list_keyword_filtered = list(set(final_list_keyword))
                f = open(path_results + keyword_filename_final, 'w' )
                for k in range(0, len(final_list_keyword_filtered)):
                    f.write(final_list_keyword_filtered[k]+"\n")
                f.close()                




                ### writing the found sources to a global pool

                #creating or loading the file to append the new sources found:
                if os.path.exists(str(path_results +'new_links_medium.dat')) == True:
                    f = open(path_results + 'new_links_medium.dat', 'a' )
                else:
                    f = open(path_results + 'new_links_medium.dat', 'w' )
                for k in range(0, len(new_sources_list)):
                    f.write(new_sources_list[k]+"\n")
                f.close()     


                # reading the file to eliminate duplicates:
                final_list = []
                f = open(str(path_results + 'new_links_medium.dat'), 'r')
                for line in f:
                    line = line.strip()
                    final_list.append(line)
                f.close()    


                # writing the de-duplicated source list to a final file:
                final_list_filtered = list(set(final_list))
                f = open(path_results + 'new_links_medium_filtered.dat', 'w' )
                for k in range(0, len(final_list_filtered)):
                    f.write(final_list_filtered[k]+"\n")
                f.close()





                print('Lenght new source list: ', len(final_list_filtered))
                print(' ')
                print(' ')


                   
            except Exception as ex:
                
                #message for specification of error

                template = "An exception of type {0} occurred. \nArguments:\n{1!r}"
                print('')
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print('')
                print('')

                filename = 'failed_keywords_medium.dat'
                #verification folder exists
                if os.path.exists(str(path_results)) == True:                    
#                     print('The folder exists')
                    
                    if os.path.exists(str(path_results + filename)) == True:
                        f = open(path_results + filename, 'a' )
                    else:
                        f = open(path_results + filename, 'w' )
                    f.write(search_term + ',' + str(j) + ',' + str(k) + "\n")
                    f.close()  
                
                else:
                                   
                    print('Folder does not exist')
                    #make folder if not exists
                    os.mkdir('results_medium_standard')

                    f = open(path_results + filename, 'w' )
                    f.write(search_term + ',' + str(j) + ',' + str(k) + "\n")
                    f.close()
                    print('Folder created')
                



                sleep_block = 600
                print(' ')
                print('Blocked by Bing! Now sleeping for {} seconds'.format(sleep_block))
                print(' ')
                time.sleep(sleep_block)
                continue                    



    print('writing index to file...')
    #print j
    f = open(path_results + 'idx_medium_forward.dat', 'w' )
    f.write(str(j))
    f.close()        



    end_time = time.time()
    dt = end_time - start_time
    time_list.append(dt)
    total_time_forecasting = len(keywords_list)*np.mean(time_list)




    print('Step elapsed time: ', dt)
    print('Total elapsed time: ', end_time - global_start_time)    
    print('Total time forecasting: ', total_time_forecasting)
    print(' ')
    print(' ')
        
        
    
print('Total elapsed time: ', time.time() - global_start_time)    
print('Total requests:', requisicao)    
    

