# =========================================================
# HOSPITAL BED DEMAND FORECASTING — MAIN ENTRY POINT
# =========================================================

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline.master_pipeline import hospital_forecasting_pipeline


# =========================================================
# RUN PIPELINE
# =========================================================

if __name__ == "__main__":
    results = hospital_forecasting_pipeline()
