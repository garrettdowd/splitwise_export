from splitwise import Splitwise
import pandas as pd
import json
import os
import wget

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path, create_dir = False):
        self.new_path = os.path.expanduser(new_path)
        if not os.path.isdir(self.new_path) and create_dir:
            os.mkdir(self.new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)

def yes_or_no(question, default = None):
    while "the answer is invalid":
        if default == None:
            reply = str(input(question+' (y/n): ')).lower().strip()
        elif default == True:
            reply = str(input(question+' (Y/n): ')).lower().strip()
            if reply == '':
                return True
        elif default == False:
            reply = str(input(question+' (y/N): ')).lower().strip()
            if reply == '':
                return False
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False

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


def get_group_expenses(sObj, group_id = None):
    if sObj == None:
        print("No Splitwise object given")
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

    return expenses
    
def get_user_name(user):
    if user != None:
        return user.getFirstName() + " " + user.getLastName()
    else:
        return None

def download_receipt(url, folder = None):
    if folder == None:
        folder = os.getcwd()
    try:
        with cd(folder, True):
            wget.download(url)
    except:
        pass
    else:
        pass
        

def expenses_to_csv(expenses, filepath = None, include_deleted = None, download_receipts = None):

    if filepath == None:
        filepath = input("Enter filename (with .csv extension). Leave blank for default (data_export.csv). File will be saved in current directory\n")
        if not filepath:
            filepath = 'data_export.csv'

    if include_deleted == None:
        include_deleted = yes_or_no("Include deleted expenses?\n", False)

    if download_receipts == None:
        download_receipts = yes_or_no("Download all receipts to a folder in the current directory?\n", False)
        if download_receipts:
            image_path = input("Enter folder name or path for images. Leave blank for default (./images/).\n")
            if not image_path:
                image_path = 'images'

    # column_order = []
    df = []
    for expense in expenses:
        df_d = {
            'Description': expense.getDescription(),
            'Date': expense.getDate(),
            'Category': expense.getCategory().getName(),
            'Details' : expense.getDetails(),
            'Cost': expense.getCost(),
            'Currency': expense.getCurrencyCode(),
            'Receipt': str(expense.getReceipt().getOriginal()),
            'Deleted': expense.getDeletedBy(),
        }
        df.append(df_d)

    df = pd.DataFrame(df)

    if download_receipts:
        df.apply(lambda row: download_receipt(row['Receipt'], image_path), axis=1)

    if include_deleted:
        df['Deleted'] = df.apply(lambda row: get_user_name(row['Deleted']), axis=1)
    else:
        # Delete these row indexes from dataFrame
        df = df[df['Deleted'].isna()]
        # Delete Column
        df = df.drop(columns=['Deleted'])
    
    # df = df.reindex(columns=column_uav)  # ensure columns are in correct order
    df.to_csv(filepath, encoding='utf-8', index=False)


def main():
    sObj = authorize()
    expenses = get_group_expenses(sObj)
    expenses_to_csv(expenses)

if __name__ == '__main__':
    main()
