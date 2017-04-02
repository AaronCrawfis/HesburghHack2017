# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 18:24:11 2017

@author: Jack Casey
"""

import datetime
import random
import requests
import re

def getOptions(eat, venue, course='Dinner', uday=0):
    
    if not eat:
        return
    else:
        if venue == 'S':
            nutr = requests.get(sdh).json()
        elif venue == 'N':
            nutr = requests.get(ndh).json()
        else:
            return
        
        target=datetime.date.today()
        target+=datetime.timedelta(days=uday)
        
        for i in range(len(nutr)):
            testdate=nutr[i]['EventStart'][0:10]
            testdate=datetime.datetime.strptime(testdate, '%Y-%m-%d')
            if testdate.day == target.day and nutr[i]['Meal'] == course:
                return nutr[i]['Courses']

#def listMeals(choices):
#    
##    meallist={}
##    sideslist={}
##    
##    for i in range(len(choices)):
##        if choices[i]['Name'] in exemptfoods:
##            continue
##        elif choices[i]['Name'] in sides:
##            for j in range(len(choices[i]['MenuItems'])):
##                food=choices[i]['MenuItems'][j]
##                foodname=food['Name']
##                foodnutr=food['NutritionURL']
##                sideslist[foodname]=NutritionLookup(foodnutr)
##        else:
##            for j in range(len(choices[i]['MenuItems'])):
##                food=choices[i]['MenuItems'][j]
##                foodname=food['Name']
##                foodnutr=food['NutritionURL']
##                meallist[foodname]=NutritionLookup(foodnutr)  
#    
#    return [sideslist, meallist]

#test = listMeals(mealoptions)
    
def getMeal(choices, fat=0, carbs=0, protein=0):
    
    sideslist=[]
    mainlist=[]
    pick = True

    for i in range(len(choices)):
        if choices[i]['Name'] in sides:
            for j in range(len(choices[i]['MenuItems'])):
                sideslist.append(choices[i]['MenuItems'][j])
        elif choices[i]['Name'] in entrees:
            for j in range(len(choices[i]['MenuItems'])):
                mainlist.append(choices[i]['MenuItems'][j])  
    
    while pick:
        sidechoice=random.choice(sideslist)
        sidename=sidechoice['Name']
        sidenutr=NutritionLookup(sidechoice['NutritionURL'])
        mainchoice=random.choice(mainlist)
        mainname=mainchoice['Name']
        mainnutr=NutritionLookup(mainchoice['NutritionURL'])
        print(sidenutr)
        print('\n')
        print(mainnutr)
        print('\n')
        totalfat = float(sidenutr['Total Fat']) + float(mainnutr['Total Fat'])
        totalcarbs = float(sidenutr['Carbohydrates']) + float(mainnutr['Carbohydrates'])
        totalprotein = float(sidenutr['Protein']) + float(mainnutr['Protein'])
        totalcals = float(sidenutr['Calories']) + float(mainnutr['Calories'])
        if totalprotein < protein:
            pick = False
    
    foodlist = [mainname, sidename, round(totalcals), 
                round(totalfat), round(totalcarbs), round(totalprotein)]
                    
    return foodlist

def NutritionLookup(url):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data=str(response.content)
    nutdict={}
    if 'Calories' not in data:
        return nutdict
    else:
        cutdata=re.sub('<[^>]+>', '', data)
        cutdata2=re.sub('&[^;]+;', '', cutdata)
        cutdata3=re.sub('Gram', ':', cutdata2)
        cutdata4=re.sub('%', ',', cutdata3)
        cutdata5=re.sub('MG', ':', cutdata4)
        cutdata5=cutdata5.replace('\\r','')
        cutdata5=cutdata5.replace('\\n','')
        cutdata5=cutdata5.replace("b'",'')
        cutdata6=re.sub('NetNutrition',' ',cutdata5)
        cutdata6=re.sub(r'.*Size:', '', cutdata6)
        cutdata7=cutdata6.lstrip()
#       cutdata7=re.sub('\   .*','   ',cutdata6)
        cutdata8=re.sub('Amount Per Serving',' ',cutdata7)
                
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
        
        if 'Contains:' in cut9:
            cut9=cut9.split('Contains:', 1)
            nutdict['Ingredients']=cut9[0]
            cut9=cut9[1]
            nutdict['Allergens']=cut9
        else:
            nutdict['Ingredients']=cut9
            nutdict['Allergens']=''
        
    return nutdict

def writetxtfile(uday=0, mealchoice):
    today=datetime.date.today()
    today+=datetime.timedelta(days=uday)
    file = open('0.txt','w')
    file.write(str(today)+'\n')
    file.write('Entree\n')
    file.write(mealchoice[0]+'\n')
    file.write('Side\n')
    file.write(mealchoice[1]+'\n')
    file.write('Calories: '+str(mealchoice[2])+'\n')
    file.write('Fat: '+str(mealchoice[3])+'\n')
    file.write('Carbohydrates: '+str(mealchoice[4])+'\n')
    file.write('Protein: '+str(mealchoice[5])+'\n')
#    file.write('Calories: '+sideselect[1]['Calories']+'\n')
#    file.write('Fat: '+sideselect[1]['Total Fat']+'\n')
#    file.write('Carbohydrates: '+sideselect[1]['Carbohydrates']+'\n')
#    file.write('Protein: '+sideselect[1]['Protein']+'\n')
    file.close()

        
sdh = 'https://www3.nd.edu/~webdev/utilities/xml2json/dining.php?feed=http%3A%2F%2Fauxopsweb2.oit.nd.edu%2FDiningMenus%2Fapi%2FMenus%2F47'
ndh = 'https://www3.nd.edu/~webdev/utilities/xml2json/dining.php?feed=http%3A%2F%2Fauxopsweb2.oit.nd.edu%2FDiningMenus%2Fapi%2FMenus%2F46'
entrees = ['Pastaria', 'Pizzeria', 'Grill', 'Mexican']
sdhentrees = ['SDH Pastaria', 'SDH Pizza', 'Pan-american', 'SDH Grill', 'SDH Asian', ]
sides=['Salads', 'Soups', 'Whole Fruits', 'Homestyle']
eat = True
venue = 'N'
protein = 20
carbs = 100
fat = 25

if __name__ == "__main__":
    mealoptions = getOptions(eat, venue)
    mealchoice=getMeal(mealoptions, fat)
    entreeselect=getEntree(mealoptions)    
    writetxtfile(0, mealchoice)
