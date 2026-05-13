# =========================================================
# MASTER HOSPITAL FORECASTING PIPELINE
# =========================================================

import time
import pandas as pd
import numpy as np
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.preprocessing_pipeline import run_preprocessing
from pipeline.forecasting_pipeline import (
    preprocess_data,
    train_icu_model,
    train_emergency_model,
    train_general_model,
    prepare_dashboard_data
)


# =========================================================
# PIPELINE FUNCTION
# =========================================================

def hospital_forecasting_pipeline():

    print("\n" + "="*60)
    print("STARTING HOSPITAL FORECASTING PIPELINE")
    print("="*60)

    pipeline_start_time = time.time()

    try:

        # -------------------------------------------------
        # STEP 1 — PREPROCESS DATA
        # -------------------------------------------------

        print("\n[1/5] Preprocessing Raw Data...")
        data = run_preprocessing()

        print("[DONE] Data preprocessing completed.")

        # -------------------------------------------------
        # STEP 2 — ICU MODEL
        # -------------------------------------------------

        print("\n[2/5] Training ICU Forecasting Model...")

        icu_results = train_icu_model(data)

        print("[DONE] ICU model training completed.")

        # -------------------------------------------------
        # STEP 3 — EMERGENCY MODEL
        # -------------------------------------------------

        print("\n[3/5] Training Emergency Forecasting Model...")

        emergency_results = train_emergency_model(data)

        print("[DONE] Emergency forecasting completed.")

        # -------------------------------------------------
        # STEP 4 — GENERAL MODEL
        # -------------------------------------------------

        print("\n[4/5] Training General Ward Forecasting Model...")

        general_results = train_general_model(data)

        print("[DONE] General ward model training completed.")

        # -------------------------------------------------
        # STEP 5 — DASHBOARD DATA
        # -------------------------------------------------

        print("\n[5/5] Preparing Dashboard Data...")

        dashboard_data = prepare_dashboard_data(data)

        print("[DONE] Dashboard data prepared.")

        # -------------------------------------------------
        # PIPELINE EXECUTION TIME
        # -------------------------------------------------

        pipeline_end_time = time.time()

        total_time = round(
            pipeline_end_time - pipeline_start_time,
            2
        )

        print("\n" + "="*60)
        print("PIPELINE EXECUTED SUCCESSFULLY")
        print(f"Total Execution Time: {total_time} seconds")
        print("="*60)

        # -------------------------------------------------
        # RETURN RESULTS
        # -------------------------------------------------

        return {

            "ICU_Model": icu_results,

            "Emergency_Model": emergency_results,

            "General_Model": general_results,

            "Dashboard_Data": dashboard_data
        }

    # -----------------------------------------------------
    # EXCEPTION HANDLING
    # -----------------------------------------------------

    except Exception as error:
        import traceback
        traceback.print_exc()
        print("\n" + "="*60)
        print("PIPELINE EXECUTION FAILED")
        print(f"ERROR: {error}")
        print("="*60)

        return None


# =========================================================
# RUN PIPELINE
# =========================================================

if __name__ == "__main__":
    results = hospital_forecasting_pipeline()
