#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 11:14:34 2020
GIThub up loader
@author: CarbonChemE
"""

from github import Github
import os
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('GITHUB_TOKEN', '...')
g = Github(token)

# want to feed in a dict of path and
def updateGraphs(pathPage,repoRef="CarbonChemE/Graphs"):
         
    #paths=['NRoom.html','PStore.html']
    # need to feed in the pages in dict format {NRoom.html:'Actual HTML...",....}
    
    repo = g.get_repo(repoRef)
       
    sha={}
    commits=list(repo.get_commits())
    
    for path in pathPage.keys():
        
        for commit in commits:
            try:
                if commit.raw_data['files'][0]['filename'] == path:
                    sha[path] = commit.raw_data['files'][0]['sha']
                    break
                continue
            except:
                continue
        
    for path in pathPage.keys():
        repo.update_file(path,'new graph',pathPage[path],sha[path],branch='main') 