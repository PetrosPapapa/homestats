import base64
import io
import pandas as pd
import config

from transactions import categorize

class InvalidTransactionFile(Exception):
    pass

expected_columns = ["Date", "Type", "Description", "Value", "Balance", "Account Name", "Account Number"]

def parse_file(filename, contents):
    if 'csv' in filename:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = parse_csv(io.StringIO(decoded.decode('utf-8')))
        return df
    else:
        raise InvalidTransactionFile("Not a csv file")

    
def parse_csv(content):
   df = pd.read_csv(
       content, 
       parse_dates=['Date'], 
       dayfirst=True,
       index_col=False,
       na_values=[''],
       escapechar="\'",
       skipinitialspace=True
   )

   # Check columns are as expected
   actual_columns = list(df.columns.values)
   if (expected_columns != actual_columns):
       raise InvalidTransactionFile("Invalid columns: " + str(actual_columns) + " - need: " + str(expected_columns) )
   
   # Strip "balance" rows
   df = df[df["Type"].notna()]
   df = df[df["Type"] != "STATEMENT"]
   
   # Inverse credit card values
   df.loc[df['Account Number'].str.startswith("5434"), 'Value'] = -df['Value']

   # Format date
   df["Date"] = df["Date"].dt.date # see https://community.plotly.com/t/datatable-datetime-format/31091/8
   
   # Sort by date
   df = df.sort_values(by=["Date"], ascending=True)
   
   # Add category
   regexes = config.db.getCategoryRegexes()
   df['Category'] = df.apply (lambda row: categorize(row['Description'], regexes), axis=1)
   
   # Unknown positives are income
   df.loc[(df['Category']=="UNKNOWN") & (df['Value']>0), 'Category'] = "INCOME"
   
   return df
