from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

REPORT_PATH = "reports/report.html"
OUTPUT_PATH = "reports/mail_report.html"

# ---------- SAFETY CHECK ----------
if not os.path.exists(REPORT_PATH):
    raise FileNotFoundError("report.html not found. Tests may not have run.")

# ---------- READ REPORT ----------
with open(REPORT_PATH, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

container = soup.find(id="data-container")
if not container or not container.get("data-jsonblob"):
    raise ValueError("data-jsonblob not found in report.html")

data = json.loads(container["data-jsonblob"])

# ---------- PARSE TEST DATA ----------
rows = ""
total = passed = failed = skipped = 0

for file, tests in data.get("tests", {}).items():
    for t in tests:
        total += 1
        status = t.get("result", "Unknown")
        duration = t.get("duration", "-")
        test_name = t.get("testId", "N/A")

        if status == "Passed":
            passed += 1
            bg_color = "#28a745"   # green
        elif status == "Failed":
            failed += 1
            bg_color = "#c62828"   # red
        elif status == "Skipped":
            skipped += 1
            bg_color = "#f9a825"   # yellow
        else:
            bg_color = "#616161"

        rows += f"""
        <tr>
            <td style="padding:6px">{test_name}</td>
            <td align="center" style="padding:6px;background-color:{bg_color};color:white;">
                {status}
            </td>
            <td style="padding:6px;text-align:center">
                {duration}
            </td>
        </tr>
        """

# ---------- HTML TEMPLATE ----------
now = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

html = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
</head>

<body style="font-family: "Poppins", sans-serif;">

<div align="center" style="width:100%">
    <h3>Pytest Automation Execution Report</h3>
</div>

<p>📌 Detailed Test Results</p>

<table border="1" cellpadding="6" cellspacing="0" width="100%"
       style="border-collapse:collapse;margin-bottom:35px">
<tr style="background:#002060;color:white">
    <th align="left">Test Name</th>
    <th align="center">Status</th>
    <th align="center">Duration</th>
</tr>
{rows}
</table>

<p>📊 Total Test Summary</p>

<table border="1" cellpadding="6" cellspacing="0" width="100%"
       style="border-collapse:collapse;">
<tr style="background:#002060;color:white">
    <th align="center">Total</th>
    <th align="center">Passed</th>
    <th align="center">Failed</th>
    <th align="center">Skipped</th>
</tr>
<tr>
    <td align="center">{total}</td>
    <td align="center" style="color:#2e7d32;">{passed}</td>
    <td align="center" style="color:#c62828;">{failed}</td>
    <td align="center" style="color:#f9a825;">{skipped}</td>
</tr>
</table>

<p style="margin-top:15px;font-size:12px;color:#666">
Detailed CSV report is attached for reference.
</p>

</body>
</html>
"""

# ---------- WRITE OUTPUT ----------
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Mail HTML generated successfully:", OUTPUT_PATH)
