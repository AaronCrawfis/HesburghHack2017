# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 18:24:11 2017
@author: Jack Casey
"""

import datetime
import random
import requests
import re
import os.path

def getOptions(eat, venue, course, uday=0):
    
    if not eat:
        return
    else:
        if venue == 'ndh':
            nutr = requests.get(ndh).json()
        else:
            nutr = requests.get(sdh).json()
        
        target=datetime.date.today()
        target+=datetime.timedelta(days=uday)

        day = target.strftime("%A")
        if (day == 'Sunday' or day == 'Saturday') and (course == 'Lunch'):
            course = 'Brunch'
        if (day == 'Sunday' or day == 'Saturday') and (course == 'Breakfast'):
            course = 'Continental Breakfast'
        
        for i in range(len(nutr)):
            testdate=nutr[i]['EventStart'][0:10]
            testdate=datetime.datetime.strptime(testdate, '%Y-%m-%d')
            if testdate.day == target.day and nutr[i]['Meal'] == course:
                return nutr[i]['Courses']
    
def getMeal(choices, course, venue):
    
    sideslist=[]
    mainlist=[]

    if venue == 'ndh':
        if course=='Breakfast' or course == 'Continental Breakfast':
            sides=ndh_b_side
            entrees=ndh_b_main
            notsides=notsides_b
            notmains=notmains_b
        elif course=='Lunch' or course == 'Brunch':
            sides=ndh_l_side
            entrees=ndh_l_main
            notsides=notsides_l
            notmains=notmains_l
        else:
            sides=ndh_d_side
            entrees=ndh_d_main
            notsides=notsides_d
            notmains=notmains_d
        for i in range(len(choices)):
            if choices[i]['Name'] in sides:
                for j in range(len(choices[i]['MenuItems'])):
                    if choices[i]['MenuItems'][j]['Name'] in notsides:
                        continue
                    else:
                        sideslist.append(choices[i]['MenuItems'][j])
            elif choices[i]['Name'] in entrees:
                for j in range(len(choices[i]['MenuItems'])):
                    if choices[i]['MenuItems'][j]['Name'] in notmains:
                        continue
                    else:
                        mainlist.append(choices[i]['MenuItems'][j])
    else:
        if course=='Breakfast' or course == 'Continental Breakfast':
            sides=sdh_b_side
            entrees=sdh_b_main
            notsides=notsides_b
            notmains=notmains_b
        elif course=='Lunch' or course == 'Brunch':
            sides=sdh_l_side
            entrees=sdh_l_main
            notsides=notsides_l
            notmains=notmains_l
        else:
            sides=sdh_d_side
            entrees=sdh_d_main
            notsides=notsides_d
            notmains=notmains_d
        for i in range(len(choices)):
            if choices[i]['Name'] in sides:
                for j in range(len(choices[i]['MenuItems'])):
                    if choices[i]['MenuItems'][j]['Name'] in notsides:
                        continue
                    else:
                        sideslist.append(choices[i]['MenuItems'][j])
            elif choices[i]['Name'] in entrees:
                for j in range(len(choices[i]['MenuItems'])):
                    if choices[i]['MenuItems'][j]['Name'] in notmains:
                        continue
                    else:
                        mainlist.append(choices[i]['MenuItems'][j])
    
    sidechoice=random.choice(sideslist)
    sidename=sidechoice['Name']
    sidenutr=NutritionLookup(sidechoice['NutritionURL'])
    mainchoice=random.choice(mainlist)
    mainname=mainchoice['Name']
    mainnutr=NutritionLookup(mainchoice['NutritionURL'])
    while type(sidenutr) != dict:
        #sideslist.remove(sidename)
        sidechoice=random.choice(sideslist)
        sidename=sidechoice['Name']
        sidenutr=NutritionLookup(sidechoice['NutritionURL'])
    while type(mainnutr) != dict:
        #mainlist.remove(mainname)
        mainchoice=random.choice(mainlist)
        mainname=mainchoice['Name']
        mainnutr=NutritionLookup(mainchoice['NutritionURL'])

    totalfat = float(sidenutr['Total Fat']) + float(mainnutr['Total Fat'])
    totalcarbs = float(sidenutr['Carbohydrates']) + float(mainnutr['Carbohydrates'])
    totalprotein = float(sidenutr['Protein']) + float(mainnutr['Protein'])
    totalcals = float(sidenutr['Calories']) + float(mainnutr['Calories'])
    
    foodlist = [mainname, sidename, round(totalcals), 
                round(totalfat), round(totalcarbs), round(totalprotein)]
                    
    return foodlist

def NutritionLookup(url):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data=str(response.content)
    nutdict={}
    if 'Calories' not in data:
        nutdict=0
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

def writetxtfile(mealchoice, course, uday=0):
    filename = '/var/www/food/food/uploads/' + str(uday) + '.txt'
    today=datetime.date.today()
    today+=datetime.timedelta(days=uday)
    file = open(filename,'a')
    file.write(str(today)+'\n')
    file.write(course+'\n')
    file.write('Entree\n')
    file.write(mealchoice[0]+'\n')
    file.write('Side\n')
    file.write(mealchoice[1]+'\n')
    file.write('Calories: '+str(mealchoice[2])+'\n')
    file.write('Fat: '+str(mealchoice[3])+'\n')
    file.write('Carbohydrates: '+str(mealchoice[4])+'\n')
    file.write('Protein: '+str(mealchoice[5])+'\n')
    file.close()

        
sdh = 'https://www3.nd.edu/~webdev/utilities/xml2json/dining.php?feed=http%3A%2F%2Fauxopsweb2.oit.nd.edu%2FDiningMenus%2Fapi%2FMenus%2F47'
ndh = 'https://www3.nd.edu/~webdev/utilities/xml2json/dining.php?feed=http%3A%2F%2Fauxopsweb2.oit.nd.edu%2FDiningMenus%2Fapi%2FMenus%2F46'
sdh_b_main=['Entrees', 'SDH Grill']
ndh_b_main=['Entrees']
sdh_b_side=['Breads & Pastries', 'Salads', 'Starches']
ndh_b_side=['Breads & Pastries', 'Salads', 'Fruit', 'Whole Fruit']
ndh_l_main=['Entrees', 'Pastaria', 'Pizzeria', 'Grill', 'Mexican', 'Asian']
sdh_l_main=['SDH Pastaria', 'SDH Pizza', 'Pan-american', 'SDH Grill', 'SDH Asian', 'Entrees']
ndh_l_side=['Salads', 'Soups', 'Whole Fruits', 'Homestyle']
sdh_l_side=['Salads', 'Soups', 'Vegetables', 'SDH Homestyle']
ndh_d_main=['Entrees', 'Pastaria', 'Pizzeria', 'Grill', 'Mexican', 'Asian']
sdh_d_main=['SDH Pastaria', 'SDH Pizza', 'Pan-american', 'SDH Grill', 'SDH Asian', 'Entrees']
ndh_d_side=['Salads', 'Soups', 'Whole Fruits', 'Homestyle']
sdh_d_side=['Salads', 'Soups', 'Vegetables', 'SDH Homestyle']

notmains_d=['Stealth French Fries', 'Thin Spaghetti', 
          'Garlic Parmesan Breadsticks', 'Tomato & Basil Marinara Sauce',
          'Buttermilk Ranch Dressing', 'Chunky Bleu Cheese Dressing',
          'Carrot Stick', 'Celery Sticks',]
notsides_d=['Pesto Salmon', 'Honey Ginger Pork Loin', 'Pork Gravy']
notmains_l=['Hard Cooked Eggs', 'Turkey Meat Sauce',
            'Bob Evans Sausage Gravy', 'Stealth French Fries',
            'Garlic Parmesan Breadsticks', "Potatoes O'Brien",
            'Classic Waffle & Pancake Syrup','Smoothie Station',
            'Tomato & Basil Marinara Sauce', 'Biscuits',
            "Hilda's Mexican Rice", 'Fried Onion Rings', 
            'Fried Seasoned Potato Cubes', 'Marinara Sauce']
notsides_l=['Peppered Pan Gravy', 'Brown Sauce','Gourmet Cinnamon Rolls',
            'Chicken Fried Steak', 'Crepe Bar', 'Pork Rub', 
            'Shrimp Spaghetti']
notmains_b=[]
notsides_b=[]

eat = True
course = 'Lunch'
venue = 'sdh'
protein = 20
carbs = 40
fat = 25

def structfromFile():
    
    biglist=[]
    for i in range(7):
        foodstruct1, foodstruct2, foodstruct3 = {},{},{}
        bigstruct={}
        if os.path.isfile('/var/www/food/food/uploads/' + str(i) + '.txt'):
            f=open('/var/www/food/food/uploads/' + str(i) + '.txt')
            lines=f.readlines()
            day=datetime.datetime.strptime(lines[0].rstrip(), '%Y-%m-%d')
            day=day.strftime("%A")
            bigstruct['Name']=day
            if len(lines) > 0:
                foodstruct1['Entree']=lines[3].rstrip()
                foodstruct1['Side']=lines[5].rstrip()
                for j in range(6,10):
                    line=lines[j].split(':')
                    #print line
                    if len(line) > 1:
                        foodstruct1[line[0].rstrip()]=line[1].lstrip().rstrip()
            if len(lines) > 10:
                foodstruct2['Entree']=lines[13].rstrip()
                foodstruct2['Side']=lines[15].rstrip()
                for j in range(16,20):
                    #print str(j) + ' (' + str(i) + ')'
                    line=lines[j].split(':')
                    if len(line) > 1:
                        foodstruct2[line[0].rstrip()]=line[1].lstrip().rstrip()
            if len(lines) > 21:
                foodstruct3['Entree']=lines[23].rstrip()
                foodstruct3['Side']=lines[25].rstrip()
                for j in range(26,30):
                    line=lines[j].split(':')
                    if len(line) > 1:
                        foodstruct3[line[0].rstrip()]=line[1].lstrip().rstrip()
            blankCourse = {'Entree':'','Side':'','Calories':'','Protein':'','Carbs':'','Fat':''}
            if foodstruct1:
                bigstruct[lines[1].rstrip()]=foodstruct1
            if foodstruct2:
                bigstruct[lines[11].rstrip()]=foodstruct2
            if foodstruct3:
                bigstruct[lines[21].rstrip()]=foodstruct3

            for c in 'Breakfast', 'Lunch', 'Dinner':
                if c not in bigstruct.keys():
                    bigstruct[c] = blankCourse

            biglist.append(bigstruct)
            
    return biglist

if __name__ == "__main__":
    mealoptions = getOptions(eat, venue, course)
    mealchoice=getMeal(mealoptions, course, venue)
#    writetxtfile(mealchoice, course)
