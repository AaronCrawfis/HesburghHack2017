# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 18:24:11 2017

@author: Jack Casey
"""

import requests
import re
        
url = 'https://www3.nd.edu/~webdev/utilities/xml2json/dining.php?feed=http%3A%2F%2Fauxopsweb2.oit.nd.edu%2FDiningMenus%2Fapi%2FMenus%2F47'
nutr = requests.get(url).json()

def getMeals(nutr, course='Dinner', days=0):
    
    for meal in nutr:
        if meal['Meal'] == course:
            return meal['Courses']

test = getMeals(nutr)

def NutritionLookup(url):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data=str(response.content)
    cutdata=re.sub('<[^>]+>', '', data)
    cutdata2=re.sub('&[^;]+;', '', cutdata)
    cutdata3=re.sub('Gram', ':', cutdata2)
    cutdata4=re.sub('%', ',', cutdata3)
    cutdata5=re.sub('MG', ':', cutdata4)
    cutdata5=cutdata5.replace('\\r\\n','')
    cutdata6=re.sub(r'.*Size:', '', cutdata5)
    cutdata7=re.sub('\   .*','   ',cutdata6)
    cutdata8=re.sub('Amount Per Serving',' ',cutdata7)
    nutdict={}
    
    cut9=cutdata8.split(' Calories:', 1)
    nutdict['Serving Size']=cut9[0]
    cut9=cut9[1]
    
    cut9=cut9.split('Calories from Fat:', 1)
    nutdict['Calories']=cut9[0]
    cut9=cut9[1]
    
    cut9=cut9.split(', Daily ValueTotal Fat:', 1)
    nutdict['Calories from Fat']=cut9[0]
    cut9=cut9[1]
    
    nutrients=['Total Fat', 'Saturated Fat', 'Trans Fat', 'Cholesterol', 
               'Sodium', 'Potassium', 'Carbohydrates', 'Fiber', 
               'Sugar', 'Protein']
    
    for i in range(0,10):
        cut9=cut9.split(':', 2)
        nutdict[nutrients[i]]=cut9[0]
        cut9=cut9[2]
    
    cut9=cut9.split(',Vitamin C:', 1)
    nutdict['Vitamin A']=cut9[0]
    cut9=cut9[1]
    
    cut9=cut9.split(',Calcium:', 1)
    nutdict['Vitamin C']=cut9[0]
    cut9=cut9[1]
    
    cut9=cut9.split(',Iron:', 1)
    nutdict['Calcium']=cut9[0]
    cut9=cut9[1]
    
    cut9=cut9.split(',Ingredients:', 1)
    nutdict['Iron']=cut9[0]
    cut9=cut9[1]
    
    cut9=cut9.split('Contains:', 1)
    nutdict['Ingredients']=cut9[0]
    cut9=cut9[1]
    
    nutdict['Allergens']=cut9
    
    return nutdict

#url = "https://nutrition.nd.edu/ScanResult.aspx/S2/0/35381"
#url2 = "https://nutrition.nd.edu/ScanResult.aspx/S2/0/152041"
#abc = NutritionLookup(url2)

