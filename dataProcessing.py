# -*- coding: utf-8 -*-
# @Time    : 4/5/21 4:28 AM
# @Author  : Kay
# @Email   : kahy.shen@gmail.com
# @File    : newDataCtree.py
# @Desc    :

import pandas as pd
import numpy as np
wpDict = {'0 - Worst possible': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9': 4, '10 - Best possible': 10}
e10Dict = {'1 - Extremely dissatisfied': 1.0, '2': 2.0, '3': 3.0, '4': 4.0, '5 - Extremely satisfied': 5.0, "Don't know/Does not apply": np.nan}
education = {"Four year bachelor's degree from a college or university (e.g.,BS,BA,AB)": "BS", 'Some postgraduate or professional schooling after graduating college,but no post': 'other', 'High school graduate (Grade 12 with diploma or GED certificate)': "High school", 'Two year associate degree from a college,university,or community college': 'other', 'Technical,trade,vocational or business school or program after high school': 'other', "Postgraduate or professional degree,including master's,doctorate,medical,or law": "Postgraduate", 'Some college,college,university,or community college -- but no degree': "other", 'Less than a high school diploma (Grades 1 through 11 or no schooling)': "Less than high school"}
# education = {"Four year bachelor's degree from a college or university (e.g.,BS,BA,AB)": 4, 'Some postgraduate or professional schooling after graduating college,but no post': 5, 'High school graduate (Grade 12 with diploma or GED certificate)': 1, 'Two year associate degree from a college,university,or community college': 6, 'Technical,trade,vocational or business school or program after high school': 3, "Postgraduate or professional degree,including master's,doctorate,medical,or law": 7, 'Some college,college,university,or community college -- but no degree': 2, 'Less than a high school diploma (Grades 1 through 11 or no schooling)': 0}

trustDict = {'1 - Strongly disagree': 'No', '2': 'No', '3': 'No', '4': 'Yes', '5 - Strongly agree': 'Yes'}

yesNoDict = {'Yes': 1, 'No': 0}
# GenderDict = {'Female': 1, 'Male': 0}
employed = {'Employed full-time (i.e. worked at least 35 hours for pay)': 'Full-time', 'Retired': 'Not-in-labor-force',
            'Employed part-time (i.e. worked less than 35 hours for pay)': 'Part-time', 'A homemaker': 'Not-in-labor-force',
            'Unemployed/laid off but looking for work': 'Involuntary-unemployed',
            'Unemployed/laid off and not looking for work': 'Not-in-labor-force',
            'A full-time student': 'Not-in-labor-force'}

# ethnic = {'White': 0, 'Hispanic': 1, 'Black': 2, 'Asian': 3, 'Other': 4}
household = {'Less than $12,000': 0, '$180,000 to $239,999': 8, '$60,000 to $89,999': 5, '$36,000 to $47,999': 3, '$120,000 to $179,999': 7, '$240,000 and over': 9, '$24,000 to $35,999': 0, '$12,000 to $23,999': 0, '$90,000 to $119,999': 6, '$48,000 to $59,999': 3}



def readFile(filename):
    # f = codecs.open(filename, 'r', 'utf8', 'ignore')

    df = pd.read_stata(filename)
    return df

if __name__ == '__main__':
    dtaFIle2 = readFile("/Users/keshen/Documents/ISI/Covid/covidSurvey/Gallup0321/"
                        "COVID_19_PANEL_SURVEY_FINAL_WEIGHTED_PUBLIC_20210321.dta")
    # print(dtaFIle2.columns.values)
    ctreeData = dtaFIle2.loc[:, ['DEMO_GENDER', 'DEMO_AGE', 'DEMO_RACE_2015_NEW', 'DEMO_EDUCATION_2017',
                                 'E1_3', 'D9', 'C82', 'C83A', 'D8_2']]

    ctreeData['E1_3'].replace(employed, inplace=True)


    # selfPositive = ctreeData.loc[:, 'ILI7_3'].values.tolist()
    # familyPositive = ctreeData.loc[:, 'ILI13_3'].values.tolist()
    # ili = []
    # for i in range(len(selfPositive)):
    #     if selfPositive[i] == 'Yes' or familyPositive[i] == 'Yes':
    #         ili.append(1)
    #     else:
    #         ili.append(0)
    # dtaFIle2['positiveTest'] = ili


    ctreeData['C83A'].replace(trustDict, inplace=True)
    # print(ctreeData['C83A'].dropna(axis=0, how='any').values)
    ctreeData['D9'].replace(household, inplace=True)
    ctreeData['DEMO_EDUCATION_2017'].replace(education, inplace=True)
    print(ctreeData.shape)
    covid = ctreeData.dropna(axis=0, how='any')
    print(covid.shape)
    # covid['DEMO_RACE_2015_NEW'].replace(ethnic, inplace=True)
    ages = covid.loc[:, 'DEMO_AGE'].values.tolist()
    # print(covid.columns.values)
    age_category = []
    for x in ages:
        if int(x) < 25:
            age_category.append(0)
        elif 25 <= int(x) <= 54:
            age_category.append(1)
        elif 55 <= int(x) <= 64:
            age_category.append(2)
        else:
            age_category.append(3)
    covid['age_category'] = age_category
    # print(set(covid.loc[:, 'DEMO_EDUCATION_2017'].values.tolist()))
    covid.rename(columns={'DEMO_GENDER': 'gender', 'D9': 'annual_household_income',
                          'DEMO_AGE': 'age', 'DEMO_RACE_2015_NEW': 'ethnicity', 'E1_3': 'employed_situation',
                          'C82': 'vaccine', 'DEMO_EDUCATION_2017': 'education', 'D8_2': 'party',
                          'C83A': 'trust_in_government'},
                 inplace=True)
    covid.to_csv("/Users/keshen/Desktop/covidR_(3.21).csv")
    # # print(ctreeData[['DEMO_RACE_2015_NEW', 'C82']].dropna(axis=0, how='any')['gender'].value_counts())
    # # covid = ctreeData[['DEMO_RACE_2015_NEW', 'C82']].dropna(axis=0, how='any')
    # print(covid['ethnicity'].value_counts())
    # print(covid[(covid['ethnicity'] == 'Other') & (covid['vaccine'] == 1.0)].shape)
    #
    # # for index, rows in groups.iterrows():
    # #     mx = max([rows['C79A'], rows['C79B'], rows['C79C']])
    # #     m = random.sample([i for i, j in enumerate([rows['C79A'], rows['C79B'], rows['C79C']]) if j == mx], 1)
    # #     agreementDict[m[0]] += 1
    # # print(agreementDict)
    # # covid.to_csv("/Users/keshen/Desktop/covidR_(4.1)_.csv")
    #
    # # print(ctreeData[['DEMO_GENDER', 'C82']].dropna(axis=0, how='any')['DEMO_GENDER'].value_counts())
    #
    #
