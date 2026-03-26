import gspread
import pandas as pd
import numpy as np
from typing import List, Dict

def get_work_records(spreadsheet_name: str = "TaskPlanning",
                     worksheet_name: str = "Mar26_TimeSpnt",
                     week_number: int = None) -> List[Dict]:
    """
    Fetches work records and optionally filters by ISO week number.
    """

    try:
        # ... (Previous authentication and data fetching steps remain the same) ...
        filename='..\..\..\credentials.json';
        print(f"{filename}")
        gc = gspread.service_account(filename)
        sh = gc.open(spreadsheet_name) 
        worksheet = sh.worksheet(worksheet_name)

        all_data_raw = worksheet.get_all_values()[1:]
        print(all_data_raw)
        all_data = [row[2:8] for row in all_data_raw]

        raw_headers = ['Day_Col', 'Date', 'ID', 'Task', 'Project', 'hrs']
        df = pd.DataFrame(all_data, columns=raw_headers)

        # Clean dates
        df['Date'] = df['Date'].replace('', np.nan).fillna(method='ffill')

        # Convert to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Remove rows with empty tasks
        df = df[df['Task'] != ''].reset_index(drop=True)

        # 1. Rename columns to match desired output keys (before mapping)
        df_mapped = df.rename(columns={
            'Date': 'date',
            'ID': 'task_id',
            'Task': 'task_des',
            'Project': 'project_name',
            'hrs': 'hours'
        })

        # 2. Define the project mapping rules
        # Key = Old Name from Google Sheet
        # Value = New standardized name/ID
        project_name_map = {
            'MCT': 'PXM010',
            'POE54': '61DE-62527',
            'XCSP': 'XCSP', # This one remains the same
            'NCAR': 'Z-08535'
        }
        # 3. Apply the mapping using Pandas replace method
        df_mapped['project_name'].replace(project_name_map, inplace=True)

        # --- FILTER BY WEEK NUMBER ---
        if week_number is not None:       
            df_mapped['egypt_week'] = df_mapped['date'].apply(sunday_week_number)
            df_mapped = df_mapped[df_mapped['egypt_week'] == week_number-1]
            print(df_mapped)
        # Final output
        final_df = df_mapped[['date', 'task_id', 'task_des', 'project_name', 'hours']]
        final_df['date'] = final_df['date'].dt.strftime('%Y-%m-%d')
        return final_df.to_dict(orient='records')

    except Exception as e:
        print(f"An error occurred during data retrieval: {e}")
        return []
    
def sunday_week_number(dt: pd.Timestamp) -> int:
    # shift Sunday to be the first day of the week
    # dt.weekday(): Mon=0 ... Sun=6
    # For Egypt: Sun=0 ... Sat=6
    adjusted = dt - pd.to_timedelta((dt.weekday() + 1) % 7, unit="D")
    return adjusted.isocalendar().week
# Example of how to run this function if you execute this script directly
if __name__ == "__main__":
    records = get_work_records(week_number=11)
    print(f"Fetched {len(records)} records.")
    # You can loop through the records here if you want:
    for record in records:
        print(record['task_des'])
