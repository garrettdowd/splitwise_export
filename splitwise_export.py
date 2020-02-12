from splitwise import Splitwise
import pandas as pd
import json
import os

def authorize(path_to_auth = None):
    if path_to_auth == None:
        path_to_auth = 'auth.json'
    
    if os.path.isfile(path_to_auth):
        with open(path_to_auth) as json_file:
            auth = json.load(json_file)
        sObj = Splitwise(auth['consumer_key'],auth['consumer_secret'],auth['access_token'])
    else:
        print("No pre-existing authorization found. Creating new auth")
        auth = {}
        # Go to https://secure.splitwise.com/apps/new and register the app to get your consumer key and secret
        auth['consumer_key'] = input("Please enter your consumer key:\n")
        auth['consumer_secret'] = input("Please enter your consumer secret:\n")

        sObj = Splitwise(auth['consumer_key'],auth['consumer_secret'])
        url, auth['secret'] = sObj.getAuthorizeURL()
        print("Authroize via the following URL")
        print(url)

        auth['oauth_token'] = url.split("=")[1]
        auth['oauth_verifier'] = input("Please enter the oauth_verifier:\n")

        auth['access_token'] = sObj.getAccessToken(auth['oauth_token'],auth['secret'],auth['oauth_verifier'])
        print("Successfully Authorized\n")
        sObj.setAccessToken(auth['access_token'])

        save = input("Save these credentials for future use? (y/n):\n")
        if save == "y":
            with open(path_to_auth, 'w') as outfile:
                json.dump(auth, outfile, indent=4)
        print("auth.json file has been saved in the current directory. Keep this file safe.")
    
    return sObj


def export_group(sObj, group_id = None):
    if sObj == None:
        print("No Splitwise object")
        return 0
    if group_id == None:
        groups = sObj.getGroups()
        for num,group in enumerate(groups):
            print(str(num)+": "+group.getName())
        group_num = input("Export data for which group? Enter the number here:\n")
        group_id = groups[int(group_num)].getId()

    offset = None
    limit = 999 # default limit is 20
    dated_after = None
    dated_before = None
    friendship_id = None
    updated_after = None
    updated_before = None

    expenses = sObj.getExpenses(offset,limit,group_id,friendship_id,dated_after,dated_before,updated_after,updated_before)

    filepath = input("Enter filename. Leave blank for default. File will be saved in current directory\n")
    if not filepath:
        filepath = None
    to_csv(expenses,filepath)


def to_csv(expenses, filepath = None):
    if filepath == None:
        filepath = 'data_export.csv'

    df = []
    for expense in expenses:
        df_d = {
            'Date': expense.getDate(),
            'Category': expense.getCategory().getName(),
            'Description': expense.getDescription(),
            'Details' : expense.getDetails(),
            'Cost': expense.getCost(),
            'Currency': expense.getCurrencyCode(),
            'Receipt': expense.getReceipt().getOriginal(),
        }
        df.append(df_d)

    df = pd.DataFrame(df)
    df.to_csv(filepath, encoding='utf-8', index=False)


def main():
    sObj = authorize()
    export_group(sObj)

if __name__ == '__main__':
    main()
