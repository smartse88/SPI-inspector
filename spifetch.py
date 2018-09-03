# -*- coding: utf-8 -*-
"""
@author: smartse
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
from pandas.io.json import json_normalize

def fetchspi(spi):
#visit an SPI and extract a list of unique usernames inside {{checkuser}} templates
    headers ={'user-agent': 'User:Smartse - tool for creating article lists from SPI'}
    sep = ' (talk'
    page=requests.get(spi)
    soup=BeautifulSoup(page.content,'html.parser') 
    users=[]
    socks=soup.find_all('span', attrs={'class': 'plainlinks cuEntry'}) 
    for i in socks:      
        users.append(i.text.strip().split(sep, 1)[0]) #strips html and template mess
    users=list(set(users)) # removes duplicates
    #ideally only keep this if /archive exists
    master = spi.replace('https://en.wikipedia.org/wiki/Wikipedia:Sockpuppet_investigations/','')
    if master in users: users.remove(master)
    #%%
    #join the usernames together and query whether they are blocked
    joinuser='|'.join(users)
    blockresq=requests.get(url='https://en.wikipedia.org/w/api.php?action=query&list=users&usprop=blockinfo&format=json&ususers='+joinuser, headers=headers).json()
    blo_df=json_normalize(blockresq['query'], 'users')
    blocked = list(blo_df['blockid']/blo_df['blockid'])

    #join data and sort so that blocked users print first
    df = pd.DataFrame(data=users)
    df['blocked'] = blocked
    df.columns = ['username','blocked']
    df = df.sort_values('blocked', axis=0)
    df.reset_index(drop=True)
    #%%
    #print output
    for u in range(len(df)):
        if df.iloc[u]['blocked'] == 1:
            print ('*{{userlinks|'+df.iloc[u]['username']+'}} (blocked)')
        else:
            print ('*{{userlinks|'+df.iloc[u]['username']+'}} (not blocked)')
        cre_req = requests.get(url='https://en.wikipedia.org/w/api.php?action=query&list=usercontribs&ucuser='+df.iloc[u]['username']+'&ucnamespace=0|2|118&ucshow=new&format=json').json()
        cre_df = json_normalize(cre_req['query'], 'usercontribs')
        for p in range(len(cre_df)):
            title = cre_df.iloc[p]['title']
            namespace = cre_df.iloc[p]['ns']
            if namespace == 0:
                print ('**{{la|'+title+'}}')
            elif namespace == 2:
                title = title.replace('User:','')
                if title != df.iloc[u]['username']:
                    print ('**{{lu|'+title+'}}')
            elif namespace == 118:
                title = title.replace('Draft:','')
                print ('**{{ld|'+title+'}}')


