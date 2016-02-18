"""An example of how to use the sakai module to collect an assignment.

Usage: collect.py <indir> <outdir>

where <indir> is a (unzipped) Sakai download directory
      <outdir> is a flat(ter) directory without spaces in filenames

This example assumes that students submit multiple attachments (not inline).
"""

import sakai
import sys, os, shutil

if len(sys.argv) != 3:
    sys.stderr.write("usage: collect.py <indir> <outdir>\n")
    sys.exit()
asst = sakai.Assignment(sys.argv[1])
outdir = sys.argv[2]
if not os.path.isdir(outdir):
    os.mkdir(outdir)
for netid, record in asst.records.items():
    if not os.path.isdir(os.path.join(outdir, netid)):
        os.mkdir(os.path.join(outdir, netid))
    for file in record['submission_files']:
        base = os.path.basename(file)
        dst = os.path.join(outdir, netid, base)
        # Sakai uses +1, etc. to distinguish versions,
        # and so does Google Drive. Replace + with ,
        # to avoid confusion. A fancier script would pick the latest.
        dst = dst.replace("+", ",") 
        shutil.copyfile(file, dst)
