
import os

import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# Question # 1
# ---------------------------------------------------------------------

def car_null_hypoth():
    """
    Returns a list of valid null hypotheses.
    
    :Example:
    >>> set(car_null_hypoth()) <= set(range(1,11))
    True
    """
    return [3,6]


def car_alt_hypoth():
    """
    Returns a list of valid alternative hypotheses.
    
    :Example:
    >>> set(car_alt_hypoth()) <= set(range(1,11))
    True
    """
    return [2,5]


def car_test_stat():
    """
    Returns a list of valid test statistics.
    
    :Example:
    >>> set(car_test_stat()) <= set(range(1,5))
    True
    """
    return [2,4]


def car_p_value():
    """
    Returns an integer corresponding to the correct explanation.
    
    :Example:
    >>> car_p_value() in [1,2,3,4,5]
    True
    """
    return [3]


# ---------------------------------------------------------------------
# Question #2
# ---------------------------------------------------------------------

def clean_apps(df):
    '''
    >>> fp = os.path.join('data', 'googleplaystore.csv')
    >>> df = pd.read_csv(fp)
    >>> cleaned = clean_apps(df)
    >>> len(cleaned) == len(df)
    True
    '''
    df['Size']=np.where((df['Size'].str.contains('M')),df['Size'].str[0:-1].astype(np.float64)*1000, df['Size'].str[0:-1].astype(np.float64))
    df['Installs']=df['Installs'].str.strip('+')
    df['Installs']=df['Installs'].replace(',','', regex=True).astype(np.int64)
    df['Type']=df['Type'].replace({'Free': 1, 'Paid': 0})
    df['Price']=df['Price'].str.strip('$').astype(np.float64)
    a=df['Last Updated'].str.split(',', expand=True)[1]
    df['Last Updated']=a.astype(np.int64)
    
    return df


def store_info(cleaned):
    '''
    >>> fp = os.path.join('data', 'googleplaystore.csv')
    >>> df = pd.read_csv(fp)
    >>> cleaned = clean_apps(df)
    >>> info = store_info(cleaned)
    >>> len(info)
    4
    >>> info[2] in cleaned.Category.unique()
    True
    '''
    q=cleaned
    
    w = cleaned.groupby('Last Updated')
    s=w.filter(lambda x : x.shape[0] > 100)
    s= s.groupby('Last Updated')
    s.first()
    b=s['Installs'].median()
    aa=b.idxmax()
    
    x = q.groupby('Content Rating')
    x.first()
    d=x['Rating'].min()
    bb=d.idxmax()
    
    x = q.groupby('Category')
    x.first()
    d=x['Price'].mean()
    cc=d.idxmax()
    
    z=q.loc[q['Reviews'] > 1000]
    x = z.groupby('Category')
    d=x['Rating'].mean()
    dd=d.idxmin()


    return [aa,bb,cc,dd]

# ---------------------------------------------------------------------
# Question 3
# ---------------------------------------------------------------------

def standard_units(any_numbers):
    return (any_numbers - np.mean(any_numbers))/np.std(any_numbers) 

def std_reviews_by_app_cat(cleaned):
    """
    >>> fp = os.path.join('data', 'googleplaystore.csv')
    >>> play = pd.read_csv(fp)
    >>> clean_play = clean_apps(play)
    >>> out = std_reviews_by_app_cat(clean_play)
    >>> set(out.columns) == set(['Category', 'Reviews'])
    True
    >>> np.all(abs(out.select_dtypes(include='number').mean()) < 10**-7)  # standard units should average to 0!
    True
    """
    c=cleaned[['Category','Reviews']]
    r=c.groupby(['Category']).transform(standard_units)
    c['Reviews']=r
    return c


def su_and_spread():
    """
    >>> out = su_and_spread()
    >>> len(out) == 2
    True
    >>> out[0].lower() in ['medical', 'family', 'equal']
    True
    >>> out[1] in ['ART_AND_DESIGN', 'AUTO_AND_VEHICLES', 'BEAUTY',\
       'BOOKS_AND_REFERENCE', 'BUSINESS', 'COMICS', 'COMMUNICATION',\
       'DATING', 'EDUCATION', 'ENTERTAINMENT', 'EVENTS', 'FINANCE',\
       'FOOD_AND_DRINK', 'HEALTH_AND_FITNESS', 'HOUSE_AND_HOME',\
       'LIBRARIES_AND_DEMO', 'LIFESTYLE', 'GAME', 'FAMILY', 'MEDICAL',\
       'SOCIAL', 'SHOPPING', 'PHOTOGRAPHY', 'SPORTS', 'TRAVEL_AND_LOCAL',\
       'TOOLS', 'PERSONALIZATION', 'PRODUCTIVITY', 'PARENTING', 'WEATHER',\
       'VIDEO_PLAYERS', 'NEWS_AND_MAGAZINES', 'MAPS_AND_NAVIGATION']
    True
    """
    return ['equal', 'GAME']


# ---------------------------------------------------------------------
# Question #4
# ---------------------------------------------------------------------


def read_survey(dirname):
    """
    read_survey combines all the survey*.csv files into a singular DataFrame
    :param dirname: directory name where the survey*.csv files are
    :returns: a DataFrame containing the combined survey data
    :Example:
    >>> dirname = os.path.join('data', 'responses')
    >>> out = read_survey(dirname)
    >>> isinstance(out, pd.DataFrame)
    True
    >>> len(out)
    5000
    >>> read_survey('nonexistentfile') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    FileNotFoundError: ... 'nonexistentfile'
    """
    dirs = os.listdir(dirname)
    re=pd.DataFrame()
    for file in dirs:
        fd=os.path.join(dirname, file)
        df1=pd.read_csv(fd)
        df=pd.DataFrame()
        for i in df1.columns:
            c = [character for character in i if character.isalnum()]
            c = "".join(c).lower()
            df[c]=df1[i]
        re=pd.concat([re, df])
    re=re.rename(columns={'firstname': 'first name', 'lastname': 'last name', 'jobtitle': 'job title', 'currentcompany': 'current company'})  
    re = re[['first name', 'last name', 'current company', 'job title', 'email', 'university']]
    return re


def com_stats(df):
    """
    com_stats 
    :param df: a DataFrame containing the combined survey data
    :returns: a hardcoded list of answers to the problems in the notebook
    :Example:
    >>> dirname = os.path.join('data', 'responses')
    >>> df = read_survey(dirname)
    >>> out = com_stats(df)
    >>> len(out)
    4
    >>> isinstance(out[0], int)
    True
    >>> isinstance(out[2], str)
    True
    """

    return [5, 253, 'Business Systems Development Analyst', 369]


# ---------------------------------------------------------------------
# Question #5
# ---------------------------------------------------------------------

def combine_surveys(dirname):
    """
    combine_surveys takes in a directory path 
    (containing files favorite*.csv) and combines 
    all of the survey data into one DataFrame, 
    indexed by student ID (a value 0 - 1000).

    :Example:
    >>> dirname = os.path.join('data', 'extra-credit-surveys')
    >>> out = combine_surveys(dirname)
    >>> isinstance(out, pd.DataFrame)
    True
    >>> out.shape
    (1000, 6)
    >>> combine_surveys('nonexistentfile') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    FileNotFoundError: ... 'nonexistentfile'
    """
    dirs = os.listdir(dirname)
    re=pd.DataFrame()
    for file in dirs:
        fd=os.path.join(dirname, file)
        df1=pd.read_csv(fd)
        if len(re) == 0:
            re= df1
        else:
            re=pd.merge(re, df1, how = "left")
    re=re.set_index('id')        
    return re


def check_credit(df):
    """
    check_credit takes in a DataFrame with the 
    combined survey data and outputs a DataFrame 
    of the names of students and how many extra credit 
    points they would receive, indexed by their ID (a value 0-1000)

    :Example:
    >>> dirname = os.path.join('data', 'extra-credit-surveys')
    >>> df = combine_surveys(dirname)
    >>> out = check_credit(df)
    >>> out.shape
    (1000, 2)
    """
    df1=df[['name']]
    df1['extra credit']=0
    df1['bool']= (((df.count(axis=1)-1)/(df.shape[1]-1)) >=0.75)
    for i in df.columns:
        if i != 'name' and (df[i].count()/df['name'].count()>= 0.9):
            df1['extra credit']+=1
    df1.loc[df1['bool'] == True, 'extra credit'] += 5
    df1=df1[['name', 'extra credit']]
    return df1

# ---------------------------------------------------------------------
# Question # 6
# ---------------------------------------------------------------------


def most_popular_procedure(pets, procedure_history):
    """
    What is the most popular Procedure Type for all of the pets we have in our `pets` dataset?
​
    :Example:
    >>> pets_fp = os.path.join('data', 'pets', 'Pets.csv')
    >>> procedure_history_fp = os.path.join('data', 'pets', 'ProceduresHistory.csv')
    >>> pets = pd.read_csv(pets_fp)
    >>> procedure_history = pd.read_csv(procedure_history_fp)
    >>> out = most_popular_procedure(pets, procedure_history)
    >>> isinstance(out,str)
    True
    """
    p=pets[['PetID']]
    rs=pd.merge(p, procedure_history, on ="PetID", how = "right")
    return rs.ProcedureType.mode()[0]


def pet_name_by_owner(owners, pets):
    """
    pet names by owner

    :Example:
    >>> owners_fp = os.path.join('data', 'pets', 'Owners.csv')
    >>> pets_fp = os.path.join('data', 'pets', 'Pets.csv')
    >>> owners = pd.read_csv(owners_fp)
    >>> pets = pd.read_csv(pets_fp)
    >>> out = pet_name_by_owner(owners, pets)
    >>> len(out) == len(owners)
    True
    >>> 'Sarah' in out.index
    True
    >>> 'Cookie' in out.values
    True
    """
    o=owners[['OwnerID', 'Name']]
    p=pets[['OwnerID','Name']]
    fx = {'Name_x': "first", "Name_y":lambda x: list(x) if len(x) >= 2 else x}
    r=pd.merge(o, p, on ="OwnerID", how = "right")    
    #r=r.drop(columns='OwnerID')    
    a=r.groupby("OwnerID").agg(fx)
    a=a.set_index("Name_x")["Name_y"]
    return a


def total_cost_per_city(owners, pets, procedure_history, procedure_detail):
    """
    total cost per city
​
    :Example:
    >>> owners_fp = os.path.join('data', 'pets', 'Owners.csv')
    >>> pets_fp = os.path.join('data', 'pets', 'Pets.csv')
    >>> procedure_detail_fp = os.path.join('data', 'pets', 'ProceduresDetails.csv')
    >>> procedure_history_fp = os.path.join('data', 'pets', 'ProceduresHistory.csv')
    >>> owners = pd.read_csv(owners_fp)
    >>> pets = pd.read_csv(pets_fp)
    >>> procedure_detail = pd.read_csv(procedure_detail_fp)
    >>> procedure_history = pd.read_csv(procedure_history_fp)
    >>> out = total_cost_per_city(owners, pets, procedure_history, procedure_detail)
    >>> set(out.index) <= set(owners['City'])
    True
    """
    o=owners[['OwnerID', 'City']]
    p=pets[['OwnerID','PetID']]
    r=pd.merge(o, p, on ="OwnerID", how = "right")
    r=r.drop(columns='OwnerID')
    w=pd.merge(r, procedure_history)
    q=pd.merge(w, procedure_detail)
    return q.groupby('City')['Price'].sum()



# ---------------------------------------------------------------------
# DO NOT TOUCH BELOW THIS LINE
# IT'S FOR YOUR OWN BENEFIT!
# ---------------------------------------------------------------------


# Graded functions names! DO NOT CHANGE!
# This dictionary provides your doctests with
# a check that all of the questions being graded
# exist in your code!


GRADED_FUNCTIONS = {
    'q01': [
        'car_null_hypoth', 'car_alt_hypoth',
        'car_test_stat', 'car_p_value'
    ],
    'q02': ['clean_apps', 'store_info'],
    'q03': ['std_reviews_by_app_cat','su_and_spread'],
    'q04': ['read_survey', 'com_stats'],
    'q05': ['combine_surveys', 'check_credit'],
    'q06': ['most_popular_procedure', 'pet_name_by_owner', 'total_cost_per_city']
}


def check_for_graded_elements():
    """
    >>> check_for_graded_elements()
    True
    """
    
    for q, elts in GRADED_FUNCTIONS.items():
        for elt in elts:
            if elt not in globals():
                stmt = "YOU CHANGED A QUESTION THAT SHOULDN'T CHANGE! \
                In %s, part %s is missing" % (q, elt)
                raise Exception(stmt)

    return True
