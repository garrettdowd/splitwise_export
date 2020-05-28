# splitwise_export
Python script to export more data from Splitwise include receipts. 

Currently supports exporting expenses from groups. Default export includes date, category, description, details (notes), cost, currency, and receipt.

## Quickstart
- Make sure you have Python 3 and the splitwise and pandas libraries installed. I recommend using [Anaconda](https://www.anaconda.com/distribution/#download-section).
`pip install splitwise pandas wget`

- Download splitwise_export.py from this repository

- Open Anaconda Prompt (or however you access your Python installation) and `cd` to where you downloaded `splitwise_export.py`. E.g. `cd ~/Downloads`

- To use the default options and export all expenses from a group (includes receipts) run
`python splitwise_export.py`
and follow the prompts.

- You will need to create a new app on your Spliwise account at https://secure.splitwise.com/apps/new.
Once you complete the authorization steps, an auth file will be saved so that authorization does not need to be repreated.



## Create custom script using functions in this script
To keep this simple, you should create your script in the same directory as `splitwise_export.py`. At the beginning of your script import this script using `import splitwise_export as spwe`. Then call a function with `spwe.authorize()` or `spwe.get_group_expenses()`

For example, you can run the same process as `splitwise_export.py` in your own script using
``` python
import splitwise_export as spwe

sObj = spwe.authorize()
expenses = spwe.get_group_expenses(sObj)
spwe.expenses_to_csv(expenses)

```

## Functions

- **authorize(path_to_auth = None)** - Returns a Splitwise Object (abbreviated as sObj) that can be used according to the [unofficial Splitwise Python API](https://github.com/namaggarwal/splitwise)
  - *path_to_auth* = (string) a path to the json auth file created by the `splitwise_export.py`. A relative or absolute path can be provided, the relative path is relative to the location of `splitwise_export.py`. If you save the auth file as `auth.json` in the same directory as `splitwise_export.py` then the path is simply `auth.json`. If no auth file is given then this function will interactively take the user through the process of generating an auth file. Multiple accounts can be authorized and each will return a unique sObj which can be stored and manipulated.


- **get_group_expenses(sObj, group_id = None)** - Returns an [`expenses`](https://github.com/namaggarwal/splitwise#expense) object based on the filters given. Currently the only filter is `group_id`, however creation and modification date filters could be added.
  - *sObj* = (Obj) A Splitwise Object returned from authorize()
  - *group_id* = (int) The [id of the group](https://github.com/namaggarwal/splitwise#group) of which you want to retrieve expenses. If no id is given then the function will interactively retrieve group names and ask the user to select the group.


- **expenses_to_csv(expenses, filepath = None, include_deleted = None, download_receipts = None)** - Does not return anything. Saves a csv file of expenses at given location.
  - *expenses* = (Obj) an `expenses` object returned from get_group_expenses().
  - *filepath* = (string) a relative or absolute filepath of where the csv file should be saved. Path can be relative to `splitwise_export.py`. If not path is given then it will be asked for interactively.
  - *include_deleted* = (bool) This determines whether deleted expenses will be exported. `False` will prevent deleted expenses from being exported in the csv. If nothing is provided then it will ask the user interactively.
  - *download_receipts* = (bool) This determines if receipts should be downloaded. `True` will prompt the user for a path/location of where to save the images. The default location is relative to `splitwise_export.py`.
