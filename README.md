# School Attendance Tracker

Daily attendance per class across one term.

## Question
Which class has the worst attendance trend, and is it getting better or worse?

## Answer
**S3 is the worst class at 82.1% average attendance, and it is getting worse (-2.7pp from first half to second half of term).**

- S1: Stable, high attendance
- S2: 89.9%, getting better (+1.4pp)
- S3: 82.1%, getting worse (-2.7pp) — needs follow-up
- S4: 90.4%, stable (+0.8pp)

## Files
- `attendance.csv` — daily attendance per class (60 school days)
- `attendance_analysis.py` — generates data, rolling average, chart
- `attendance_rolling.png` — 7-day rolling average chart per class
- `summary.txt` — plain-language summary

## How to run
```bash
python attendance_analysis.py
