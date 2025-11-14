#!/usr/bin/env python3
"""
SAFE your_script.py
- Loads CSVs
- Fixes duplicate columns
- Handles corrupted lead_log.csv headers
- Creates profiling_summary.csv + report.csv
"""

import os
import argparse
import pandas as pd


# ---------------- HELPERS ----------------

def read_csv_clean(path):
    df = pd.read_csv(path, dtype=str)
    df = df.fillna("")
    return df


def fix_duplicate_columns(df):
    """Make duplicate columns unique: id,id,id → id,id_2,id_3"""
    new_cols = []
    counts = {}
    for col in df.columns:
        if col not in counts:
            counts[col] = 1
            new_cols.append(col)
        else:
            counts[col] += 1
            new_cols.append(f"{col}_{counts[col]}")
    df.columns = new_cols
    return df


def profile_table(df, name):
    rows = []
    for col in df.columns:
        rows.append({
            "table": name,
            "column": col,
            "null_count": df[col].isna().sum(),
            "distinct_count": df[col].nunique(),
            "dtype": str(df[col].dtype)
        })
    return pd.DataFrame(rows)


# ---------------- MAIN ----------------

def main(data_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    # Load all files
    lead = read_csv_clean(os.path.join(data_dir, "lead_log.csv"))
    txn = read_csv_clean(os.path.join(data_dir, "paid_transactions.csv"))
    reward = read_csv_clean(os.path.join(data_dir, "referral_rewards.csv"))
    status = read_csv_clean(os.path.join(data_dir, "user_referral_statuses.csv"))
    ulog = read_csv_clean(os.path.join(data_dir, "user_logs.csv"))
    urlog = read_csv_clean(os.path.join(data_dir, "user_referral_logs.csv"))
    ur = read_csv_clean(os.path.join(data_dir, "user_referrals.csv"))

    # ---------------- FIX LEAD FILE (STRONGEST FIX) ----------------
    # Ignore whatever header is in lead_log.csv → force unique names
    lead.columns = [f"lead_col{i+1}" for i in range(len(lead.columns))]

    # Treat first column as lead_id
    lead = lead.rename(columns={"lead_col1": "lead_id"})
    # ----------------------------------------------------------------

    # Convert join keys to string
    join_cols = [
        "referrer_id", "referee_id", "referral_reward_id",
        "transaction_id", "user_referral_status_id", "referral_id"
    ]

    for col in join_cols:
        if col in ur.columns:
            ur[col] = ur[col].astype(str)

    # Fix ID names in other tables
    if "id" in status.columns:
        status = status.rename(columns={"id": "user_referral_status_id"})
    if "id" in reward.columns:
        reward = reward.rename(columns={"id": "referral_reward_id"})

    # ---------------- MERGE ----------------
    df = ur.merge(status, on="user_referral_status_id", how="left")
    df = df.merge(reward, on="referral_reward_id", how="left")
    df = df.merge(txn, on="transaction_id", how="left")

    if "user_referral_id" in urlog.columns:
        urlog = urlog.rename(columns={"user_referral_id": "referral_id"})
        df = df.merge(urlog, on="referral_id", how="left")

    # SAFE LEAD MERGE
    df = df.merge(lead, left_on="referee_id", right_on="lead_id", how="left")

    # ---------------- profiling ----------------
    profiling = []
    for name, table in [
        ("lead_logs", lead),
        ("paid_transactions", txn),
        ("referral_rewards", reward),
        ("user_referral_statuses", status),
        ("user_logs", ulog),
        ("user_referral_logs", urlog),
        ("user_referrals", ur),
    ]:
        profiling.append(profile_table(table, name))

    profiling = pd.concat(profiling)
    profiling.to_csv(os.path.join(out_dir, "profiling_summary.csv"), index=False)

    # ---------------- final output ----------------
    df.to_csv(os.path.join(out_dir, "report.csv"), index=False)

    print("🎉 SUCCESS! Created:")
    print(" - profiling_summary.csv")
    print(" - report.csv")


# ---------------- ENTRY ----------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--out-dir", default="out")
    args = parser.parse_args()
    main(args.data_dir, args.out_dir)
