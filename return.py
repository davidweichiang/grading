"""An example of how to use the sakai and sheets modules to return an assignment.

Usage: return.py <sheet> <indir> <outdir>

where <sheet> is a Google Drive spreadsheet, downloaded as HTML
      <indir> is a (unzipped) Sakai download directory
      <outdir> is a (unzipped) Sakai upload directory

Assumes that the spreadsheet just has three columns: netid, comments, and score.
"""

import sakai, sheets
import sys

if len(sys.argv) != 4:
    sys.stderr.write("usage: return.py <sheet> <indir> <outdir>")
    sys.exit()
sheet = sheets.read_sheet(sys.argv[1])
asst = sakai.Assignment(sys.argv[2])
outdir = sys.argv[3]

for row in sheet[1:]: # skip header row
    netid, comments, score = row[:3]
    if netid not in asst.records:
        sys.stderr.write("warning: no record for {}\n".format(netid))
        continue
    record = asst.records[netid]
    record['comments_html'] = comments
    record['grade'] = score
    # You could also supply the filename of a solution set here
    #record['feedback_files'] = [solution]

asst.write(outdir)
