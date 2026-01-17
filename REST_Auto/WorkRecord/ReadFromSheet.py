import gspread
import pandas as pd

# 1. Authenticate using the downloaded JSON key file
gc = gspread.service_account(filename='credentials.json')

# 2. Open the spreadsheet by its name or ID
# You can find the ID in the URL: ://docs.google.com[YOUR_ID]/edit
sh = gc.open("TaskPlanning") 

# 3. Select the specific worksheet (e.g., 'Sheet1')
worksheet = sh.worksheet("Jan26_TimeSpnt")

# 4. Fetch the value of a specific cell (e.g., F2)
cell_value = worksheet.acell('F2').value

# Print the value
print(f"The value in cell F2 is: {cell_value}")
