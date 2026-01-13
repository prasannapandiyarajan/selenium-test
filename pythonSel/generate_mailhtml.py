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
            color = "#2e7d32"   # green
        elif status == "Failed":
            failed += 1
            color = "#c62828"   # red
        elif status == "Skipped":
            skipped += 1
            color = "#f9a825"   # yellow
        else:
            color = "#616161"

        rows += f"""
        <tr>
            <td style="padding:6px">{test_name}</td>
            <td style="padding:6px;font-weight:bold;color:{color}">
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
<body style="font-family:Arial, sans-serif;">

<h2>✅ Automation Test Report</h2>
<p><b>Execution Time:</b> {now}</p>

<table cellpadding="6" cellspacing="0" width="600"
       style="border-collapse:collapse;margin-bottom:15px;">
<tr>
    <th align="left">Total</th>
    <th align="left">Passed</th>
    <th align="left">Failed</th>
    <th align="left">Skipped</th>
</tr>
<tr>
    <td>{total}</td>
    <td style="color:#2e7d32;font-weight:bold">{passed}</td>
    <td style="color:#c62828;font-weight:bold">{failed}</td>
    <td style="color:#f9a825;font-weight:bold">{skipped}</td>
</tr>
</table>

<table border="1" cellpadding="6" cellspacing="0" width="100%"
       style="border-collapse:collapse;">
<tr style="background:#f2f2f2">
    <th align="left">Test Name</th>
    <th align="center">Status</th>
    <th align="center">Duration</th>
</tr>
{rows}
</table>

<p style="margin-top:15px;font-size:12px;color:#666">
This is an auto-generated email. Please refer to Jenkins for full report and screenshots.
</p>

</body>
</html>
"""

# ---------- WRITE OUTPUT ----------
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Mail HTML generated successfully:", OUTPUT_PATH)
