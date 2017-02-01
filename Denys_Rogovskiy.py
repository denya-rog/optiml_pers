#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 09:55:16 2017

@author: denya
"""

def curriculum(personal="personal",task="task"):
    ''' checking of right input data: 
            existing of the file,
            existing of nessesary colmns'''
    import pandas as pd

    try:
        personal=pd.read_csv('{0}.csv'.format(personal),delimiter ='\t') 
    
    except:

        raise NameError('name of csv File must be:  {0}.csv '.format(personal))
    try:
    
        tasks=pd.read_csv('{0}.csv'.format(task),delimiter ='\t')
    
    except:
    
        raise NameError ('name of csv File must be:  {0}.csv  '.format(tasks))

    
    if 'nickname' not in list(personal.columns.values):
        raise NameError('create and fill  nickname')
    
    if 'task_point' not in list(personal.columns.values):
        raise NameError('create and fill task_point')
    
    if 'name' not in list(tasks.columns.values):
        raise NameError('create and fill  name')
    
    if 'task_point' not in list(tasks.columns.values):
        raise NameError('create and fill  task_point')

    
    """checking  data and filtering from bad meanings"""   

    personal=personal.drop_duplicates(['nickname'])

    personal=personal.dropna(subset=['nickname'])

    tasks['name']=tasks['name'].replace({None:'new_name_instead of none'})

    counter=1
    for i in tasks['name']:
        if i =='new_name_instead of none':

            i=i+str(counter)
            counter+=1


    tasks=tasks.drop_duplicates(['name']) 
       
    personal['task_point']=personal['task_point'].fillna(10000) 
    personal[personal['task_point']<=0]=10000
    personal['task_point']=personal['task_point'].replace({10000:min(personal['task_point'])})


    tasks['task_point']=tasks['task_point'].fillna(10000)
    for i in tasks['task_point'].index:
    
        if tasks['task_point'][i]<=0:
        
            tasks['task_point'][i]=10000

    tasks['task_point']=tasks['task_point'].replace({10000:min(tasks['task_point'])})


    """creation of new, nessesary columns""" 
    
    sum_task=sum(tasks['task_point'])
    sum_pers=sum(personal['task_point'])
    



    tasks.sort_values('task_point',inplace=True,ascending=False)
    personal.sort_values('task_point', inplace=True,ascending=False)

    if  sum_task>=sum_pers:
        personal['max_t_p']=personal['task_point']
        personal.loc[100000] = [sum_task-sum_pers for n in range(len(list(personal.columns.values)))]
        personal.loc[100000]='tomorrow'

    else:
        personal['max_t_p']=personal['task_point']*sum_task/sum_pers
        personal['max_t_p']=personal['max_t_p'].round()

    personal['defin']=(personal['max_t_p']-personal['total'])
    personal['name_task']=''


    """greedy method"""

    for j in tasks['task_point'].index:
    
        i=personal['defin'].idxmax()
    
        tasks['ID_pers'][j]=personal['nickname'][i]
        personal['total'][i]+=tasks['task_point'][j]
        personal['name_task'][i]+=str(tasks['name'][j])+","
    
        personal['defin'][i]=(personal['max_t_p'][i]-personal['total'] [i])

    print(tasks)
    print(personal)
    out=personal(columns=['nickname', 'task_point','name_task','total'])
    return(out)
curriculum()