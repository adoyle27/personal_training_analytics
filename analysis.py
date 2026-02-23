import pandas as pd
import matplotlib.pyplot as plt

EXCEL_PATH = "clean_data.xlsx"
SHEET_NAME = "Clean_Data" # first sheet


#LOAD
df_raw = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)

#Keep only the columns we actually need (ignore the dashboard tables)
needed_cols = [
    "client_id",
    "service_type",
    "ideal_hours_month",
    "hours_nov_jan",
    "30_60",
]

#some excel exports may have tiny differences like trailing spaces in headers
df_raw.columns = [c.strip() if isinstance(c, str) else c for c in df_raw.columns]

missing = [c for c in needed_cols if c not in df_raw.columns]
if missing:
    raise ValueError(f"Missing expected columns in Excel: {missing}\nFound: {list(df_raw.columns)}")

df = df_raw[needed_cols].copy()
df["30_60"] = df["30_60"].astype(str).str.strip().str.lower()
df = df[df["30_60"].isin(["hour", "thirty"])]

#drop rows that aren't part of the client table (blank/misc dashboard rows)
df = df[df["ideal_hours_month"].notna() & df["hours_nov_jan"].notna()]

#sometimes the same clients appear again because of the chart tables
df = df.drop_duplicates(subset=["client_id"], keep="first")

#clean numeric clients
df["ideal_hours_month"] = pd.to_numeric(df["ideal_hours_month"], errors="coerce")
df["hours_nov_jan"] = pd.to_numeric(df["hours_nov_jan"], errors="coerce")

#rates
RATE_HOUR = 61.20
RATE_THIRTY = 33.75

def session_rate(session_type: str) -> float:
    s = str(session_type).strip().lower()
    if s == "hour":
        return RATE_HOUR
    if s =="thirty":
        return RATE_THIRTY
    raise ValueError(f"Unexpected 30_60 value: {session_type!r} (expected 'hour' or 'thirty')")

df["session_rate"] = df["30_60"].apply(session_rate)

#Metrics (recomputed)
df["expected_hours_3mo"] = df["ideal_hours_month"] * 3
df["utilization"] = df["hours_nov_jan"] / df["expected_hours_3mo"]
df["revenue_nov_jan"] = df["hours_nov_jan"] * df["session_rate"]
df["avg_monthly_revenue"] = df["revenue_nov_jan"] / 3
df["hours_gap"] = df["expected_hours_3mo"] - df["hours_nov_jan"]
df["positive_gap"] = df["hours_gap"].clip(lower=0)

#revenue share
total_monthly = df["avg_monthly_revenue"].sum()
df["revenue_share_pct"] = df["avg_monthly_revenue"] / total_monthly

#segmentation
#high revenue: >= 5% share, hight utilization: >= 80%
df["high_revenue"] = df["revenue_share_pct"] >= 0.05
df["high_utilization"] = df["utilization"] >= 0.80

def segment(row) -> str:
    if row["high_revenue"] and row["high_utilization"]:
        return "Anchor"
    if row["high_revenue"] and not row["high_utilization"]:
        return "Opportunity"
    if (not row["high_revenue"]) and row["high_utilization"]:
        return "Steady"
    return "Low impact"

df["segment"] = df.apply(segment, axis=1)

#key summary numbers
missing_hours_3mo = df.loc[df["hours_gap"] > 0, "hours_gap"].sum()
avg_missing_hours_month = missing_hours_3mo / 3
rev_opp_per_month = avg_missing_hours_month * RATE_HOUR # rough estimate using hour rate

print("=== Summary ===")
print(f"Clients: {len(df)}")
print(f"Total avg monthly revenue: ${total_monthly:,.2f}")
print(f"Missing hours (3 months): {missing_hours_3mo:.1f}")
print(f"Avg missing hours per month: {avg_missing_hours_month:.1f}")
print(f"Rough revenue opportunity per month (hour rate): ${rev_opp_per_month:,.2f}")

#segment table
segment_summary = (
    df.groupby("segment", as_index=False)
    .agg(
        client_count=("client_id", "count"),
        avg_monthly_revenue=("avg_monthly_revenue", "sum"),
        avg_monthly_gap_hours=("positive_gap", lambda s: s.sum() / 3),
    )
    .sort_values("avg_monthly_revenue", ascending=False)
)

print("\n=== Segment Summary ===")
print(segment_summary.to_string(index=False))

#save outputs for GitHub
df.to_csv("client_metrics.csv", index=False)

#Chart 1: Avg Monthly Revenue by Segment
plt.figure()
segment_summary_plot = segment_summary.sort_values("avg_monthly_revenue", ascending=False)
plt.bar(segment_summary_plot["segment"], segment_summary_plot["avg_monthly_revenue"])
plt.title("Average Monthly Revenue by Client Segment")
plt.ylabel("Avg Monthly Revenue ($)")
plt.tight_layout()
plt.savefig("revenue_by_segment.png", dpi=200)
plt.close()

#chart 2: Unrealized Hours by Client (positive only)
gap_df = df[df["positive_gap"] > 0].sort_values("positive_gap", ascending=False)
plt.figure(figsize=(9, 4))
plt.bar(gap_df["client_id"], gap_df["positive_gap"])
plt.title("Unrealized Training Hours by Client (3 Months)")
plt.ylabel("Hours Gap (Positive Only)")
plt.xticks(rotation=90)
plt.tight_layout
plt.savefig("unrealized_hours_by_client.png", dpi=200)
plt.close()

print("\nSaved file:")
print("- client_metrics.csv")
print("- segment_summary.csv")
print("- revenue_by_segment.png")
print("- unrealized_hours_by_client.png")