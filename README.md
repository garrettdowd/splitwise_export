# splitwise_export
Export more data from Splitwise include receipts. 

Currently supports exporting expenses from groups. Default export includes date, category, description, details (notes), cost, currency, and receipt.

## Quickstart
Make sure you have splitwise and pandas installed.
`pip install splitwise pandas`

To use the default group export (includes receipts) run
`python splitwise_export.py`

You will need to create a new app on your Spliwise account at https://secure.splitwise.com/apps/new

Once you complete the authorization steps, an auth file will be saved so that authorization does not need to be repreated.
