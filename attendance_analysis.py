import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# 1. Generate realistic sample data - 1 term, 60 school days, Mon-Fri
dates = pd.bdate_range(start="2026-09-07", periods=60)
classes = ["S1", "S2", "S3", "S4"]

rows = []
for cls in classes:
    # Base attendance + trend per class
    if cls == "S1":
        base, trend = 92, 0.02 # stable high
    elif cls == "S2":
        base, trend = 89, 0.05 # slowly improving
    elif cls == "S3":
        base, trend = 86, -0.12 # worst, getting worse
    else:
        base, trend = 90, 0.03 # stable

    for i, date in enumerate(dates):
        # Weekly dip on Friday + random noise
        friday_dip = -3 if date.weekday() == 4 else 0
        noise = np.random.normal(0, 2.5)
        attendance = base + (trend * i) + friday_dip + noise
        attendance = max(70, min(99, attendance)) # keep realistic
        enrolled = 45 if cls != "S3" else 48
        present = round(enrolled * attendance / 100)
        rows.append([date.date(), cls, enrolled, present, round(attendance, 1)])

df = pd.DataFrame(rows, columns=["date", "class", "enrolled", "present", "attendance_pct"])
df.to_csv("attendance.csv", index=False)

# 2. Rolling average - 7-day rolling
df["date"] = pd.to_datetime(df["date"])
pivot = df.pivot(index="date", columns="class", values="attendance_pct")
rolling = pivot.rolling(window=7, min_periods=1).mean()

# 3. Which class is worst? + getting better or worse?
summary = []
for cls in classes:
    avg = df[df["class"] == cls]["attendance_pct"].mean()
    first_half = df[(df["class"] == cls)].head(30)["attendance_pct"].mean()
    second_half = df[(df["class"] == cls)].tail(30)["attendance_pct"].mean()
    change = second_half - first_half
    direction = "getting worse" if change < -1 else "getting better" if change > 1 else "stable"
    summary.append((cls, avg, change, direction))

worst = min(summary, key=lambda x: x[1])

print("=== ATTENDANCE SUMMARY ===")
for cls, avg, change, direction in summary:
    print(f"{cls}: Avg {avg:.1f}% | Change {change:+.1f}pp | {direction}")
print(f"\nWORST: {worst[0]} at {worst[1]:.1f}% avg, {worst[3]}")

# Save plain-language summary
with open("summary.txt", "w") as f:
    f.write("School Attendance Tracker - One Term Summary\n\n")
    for cls, avg, change, direction in summary:
        f.write(f"{cls}: Average {avg:.1f}%, changed {change:+.1f} points, {direction}.\n")
    f.write(f"\nWorst class: {worst[0]} with {worst[1]:.1f}% average attendance, and it is {worst[3]}.\n")
    f.write("Recommendation: Focus follow-up on S3 - check reasons for Friday absences and late-term drop.\n")

# 4. Chart - rolling average per class
plt.figure(figsize=(10, 6))
for cls in classes:
    plt.plot(rolling.index, rolling[cls], label=cls, linewidth=2)

plt.title("School Attendance - 7-Day Rolling Average per Class (One Term)")
plt.xlabel("Date")
plt.ylabel("Attendance % (7-day rolling avg)")
plt.ylim(75, 100)
plt.grid(True, alpha=0.3)
plt.legend(title="Class")
plt.tight_layout()
plt.savefig("attendance_rolling.png")
print("\nSaved: attendance.csv, attendance_rolling.png, summary.txt")
