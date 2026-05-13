# =========================================================
# HOSPITAL BED DEMAND FORECASTING PROJECT
# DATA PREPROCESSING PIPELINE - VERSION 3.0 (2026 DATA)
# =========================================================

import pandas as pd
import numpy as np
import os
import datetime


def run_preprocessing():
    """Preprocessing with 2026 dates leading up to 'Today'."""
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
    PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
    
    df1 = pd.read_csv(os.path.join(RAW_DIR, "hospital_insights_summary.csv"))
    df3 = pd.read_csv(os.path.join(RAW_DIR, "dataset3.csv"))

    # -----------------------------------------------------
    # DATE RE-CALIBRATION TO 2026
    # -----------------------------------------------------
    # Today is 2026-05-12. Let's make the dataset end today.
    end_date = datetime.date.today()
    num_days = len(df1)
    start_date = end_date - datetime.timedelta(days=num_days-1)
    
    df1['Date'] = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Map df3 to these new dates
    df3['Date'] = pd.to_datetime(df3['timestamp']).dt.normalize()
    # Shift df3 dates to match our target range
    old_min = df3['Date'].min()
    date_offset = pd.to_datetime(start_date) - old_min
    df3['Date'] = df3['Date'] + date_offset

    df3_agg = df3.groupby('Date').agg({
        'admissions': 'sum',
        'discharges': 'sum',
        'staff_count': 'mean',
        'flu_cases': 'sum',
        'bed_occupancy': 'mean'
    }).reset_index()

    merged = pd.merge(df1[['Date', 'service', 'avg_stay', 'recommended_staff']], df3_agg, on='Date', how='inner')
    merged.rename(columns={'admissions': 'Total_Admissions', 'staff_count': 'Staff_Count', 'bed_occupancy': 'Bed_Occupancy', 'flu_cases': 'Flu_Cases'}, inplace=True)

    # STRICT DEMAND RATIOS (15/20/65)
    merged['ICU_Demand'] = (merged['Total_Admissions'] * 0.15).round().astype(int)
    merged['Emergency_Demand'] = (merged['Total_Admissions'] * 0.20).round().astype(int)
    merged['General_Demand'] = merged['Total_Admissions'] - (merged['ICU_Demand'] + merged['Emergency_Demand'])
    merged['Admissions'] = merged['ICU_Demand'] + merged['Emergency_Demand'] + merged['General_Demand']

    output_path = os.path.join(PROCESSED_DIR, "final_hospital_forecasting_dataset.csv")
    merged.to_csv(output_path, index=False)
    print(f"Dataset updated to 2026 (Ends: {end_date}) at {output_path}")
    return merged

if __name__ == "__main__":
    run_preprocessing()
