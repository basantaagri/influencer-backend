import pandas as pd
import os
from app.db import get_supabase

# ----------------------------------------
# CONFIG
# ----------------------------------------
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "yt.csv")
TABLE_NAME = "influencers"

# ----------------------------------------
# LOAD CSV (NO MODIFICATION)
# ----------------------------------------
df = pd.read_csv(CSV_PATH)

# Replace NaN with None (Supabase-safe)
df = df.where(pd.notnull(df), None)

# ----------------------------------------
# SUPABASE CLIENT
# ----------------------------------------
supabase = get_supabase()

# ----------------------------------------
# INSERT ROWS (LOCKED SCHEMA)
# ----------------------------------------
records = df.to_dict(orient="records")

print(f"Importing {len(records)} rows into '{TABLE_NAME}' table...")

response = supabase.table(TABLE_NAME).insert(records).execute()

if response.data:
    print("✅ CSV import completed successfully.")
    print(f"✅ Rows inserted: {len(response.data)}")
else:
    print("⚠️ No rows inserted. Check table schema or permissions.")
