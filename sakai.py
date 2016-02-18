import csv
import sys, os, shutil

ignore_files = ["Icon\r", ".DS_Store"]

class Assignment(object):
    def __init__(self, root=None):
        if root:
            self.read(root)

    def read(self, root):
        root = os.path.abspath(root)
        records = {}

        # Use grades.csv as table of contents
        with open(os.path.join(root, 'grades.csv')) as gradesfile:
            grades = list(csv.reader(gradesfile))

        self.title = grades[0][0]
        self.gradetype = grades[0][1]
        self.headers = grades[2]
        for row in grades[3:]:
            displayid, eid, lastname, firstname, grade = row
            records[eid] = {}
            records[eid]['displayid'] = displayid
            records[eid]['lastname'] = lastname
            records[eid]['firstname'] = firstname
            records[eid]['grade'] = grade

            fullname = '{}, {}({})'.format(lastname, firstname, eid)
            dir = os.path.join(root, fullname)
            if os.path.isdir(dir):
                submitfile = os.path.join(dir, fullname+"_submissionText.html")
                if os.path.isfile(submitfile):
                    with open(submitfile) as sfile:
                        records[eid]['submission_html'] = sfile.read()

                submitdir = os.path.join(dir, "Submission attachment(s)")
                if os.path.isdir(submitdir):
                    records[eid]['submission_files'] = []
                    for file in os.listdir(submitdir):
                        if file in ignore_files: continue
                        records[eid]['submission_files'].append(os.path.join(submitdir, file))

                feedbackfile = os.path.join(dir, "feedbackText.html")
                if os.path.isfile(feedbackfile):
                    with open(feedbackfile) as ffile:
                        s = ffile.read()
                    # Sakai only copies the submission into the inline feedback
                    # if the grader actually types something
                    if len(s) == 0:
                        s = records[eid]['submission_html']
                    records[eid]['feedback_html'] = s

                commentsfile = os.path.join(dir, "comments.txt")
                if os.path.isfile(commentsfile):
                    with open(commentsfile) as ffile:
                        records[eid]['comments_html'] = ffile.read()

                feedbackdir = os.path.join(dir, "Feedback Attachment(s)")
                if os.path.isdir(feedbackdir):
                    records[eid]['feedback_files'] = []
                    for file in os.listdir(feedbackdir):
                        if file in ignore_files: continue
                        records[eid]['feedback_files'].append(os.path.join(feedbackdir, file))

        self.records = records

    def write(self, root):
        root = os.path.abspath(root)
        if not os.path.isdir(root):
            os.makedirs(root)
        
        # Write grades.csv
        with open(os.path.join(root, "grades.csv"), "w") as outfile:
            writer = csv.writer(outfile)
            writer.writerow([self.title, self.gradetype])
            writer.writerow([])
            writer.writerow(self.headers)

            for eid, record in sorted(self.records.items()):
                writer.writerow([record['displayid'], 
                                 eid, 
                                 record['lastname'],
                                 record['firstname'],
                                 record['grade']])

        # Write individual directories
        for eid, record in self.records.items():
            fullname = '{}, {}({})'.format(record['lastname'], 
                                           record['firstname'],
                                           eid)
            dir = os.path.join(root, fullname)
            if not os.path.isdir(dir): os.mkdir(dir)
            
            if 'submission_html' in record:
                with open(os.path.join(dir, fullname+"_submissionText.html"), 'w') as outfile:
                    outfile.write(record['submission_html'])

            if 'submission_files' in record:
                submitdir = os.path.join(dir, "Submission attachment(s)")
                if not os.path.isdir(submitdir): os.mkdir(submitdir)
                for file in record['submission_files']:
                    shutil.copyfile(file, os.path.join(submitdir, os.path.basename(file)))

            if 'feedback_html' in record:
                with open(os.path.join(dir, "feedbackText.html"), 'w') as outfile:
                    outfile.write(record['feedback_html'])
            if 'comments_html' in record:
                with open(os.path.join(dir, "comments.txt"), 'w') as outfile:
                    outfile.write(record['comments_html'])

            if 'feedback_files' in record:
                feedbackdir = os.path.join(dir, "Feedback Attachment(s)")
                if not os.path.isdir(feedbackdir): os.mkdir(feedbackdir)
                for file in record['feedback_files']:
                    shutil.copyfile(file, os.path.join(feedbackdir, os.path.basename(file)))
