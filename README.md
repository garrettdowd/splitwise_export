# splitwise_export
Python script to export more data from Splitwise include receipts. 

Currently supports exporting expenses from groups. Default export includes date, category, description, details (notes), cost, currency, and receipt.

## Quickstart
- Make sure you have Python 3 and the splitwise and pandas libraries installed. I recommend using [Anaconda](https://www.anaconda.com/distribution/#download-section).
`pip install splitwise pandas`

- Download splitwise_export.py from this repository

- Open Anaconda Prompt (or however you access your Python installation) and `cd` to where you downloaded `splitwise_export.py`. E.g. `cd ~/Downloads`

- To use the default options and export all expenses from a group (includes receipts) run
`python splitwise_export.py`
and follow the prompts.

- You will need to create a new app on your Spliwise account at https://secure.splitwise.com/apps/new.
Once you complete the authorization steps, an auth file will be saved so that authorization does not need to be repreated.
