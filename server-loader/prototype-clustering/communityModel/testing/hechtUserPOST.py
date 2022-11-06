import csv
import os
import sys

from context import dao
from dao.dao_db_users import DAO_db_users
from dao.dao_api import DAO_api
import pandas as pd

def main():
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Read HECHT user data: all users except the last one
    #--------------------------------------------------------------------------------------------------------------------------
    
    route = "data/hecht users.csv"
    df = pd.read_csv(route)
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    fill NaN values
    #--------------------------------------------------------------------------------------------------------------------------
    
    # Fill NaN values with default ones (center value or dont know if exists)
    df['beliefR'].fillna('DK',inplace=True)
    df['beliefJ'].fillna('CantJudge',inplace=True)
    df['beliefE'].fillna('Balanced',inplace=True)
    df['DemographicsPolitics'].fillna('DK',inplace=True)
    df['DemographicsReligous'].fillna('R',inplace=True)
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    remove users from database
    #--------------------------------------------------------------------------------------------------------------------------
      
    daoU = DAO_db_users()
    #daoU.drop()
    
    daoAPI = DAO_api()

    #--------------------------------------------------------------------------------------------------------------------------
    #    perform post requests with user information
    #--------------------------------------------------------------------------------------------------------------------------
    
    users = []
    for ind in df.index:
        # print(df[' '][ind], df['beleifR'][ind], df['DemographicPolitics'][ind], df['DemographicReligous'][ind])
        user = {}
        user["userid"] = df['user'][ind]
        user['_id'] = user["userid"]
        user["origin"] = ""
        user["source_id"] = ""
        user["participantType"] = str(df["Participant type"][ind]) # Participant type
        user["beleifR"] = df['beliefR'][ind]  # beleifR
        user["beliefJ"] = df['beliefJ'][ind]  # beliefJ
        user["beliefE"] = df['beliefE'][ind]  # beliefE
        user["DemographicPolitics"] = df['DemographicsPolitics'][ind]  # DemographicPolitics
        user["DemographicReligous"] = df['DemographicsReligous'][ind]  # DemographicReligous
        
        # Split user information into user model dict
        usersAPI = daoU.userToPostAPIFormat(user)

        for user in usersAPI:
            postUserData = [user]
            response = daoAPI.updateUser(user['userid'],postUserData)

    
main()
