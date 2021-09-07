# Google Classroom Scripts
 A collection of Python scripts to help school teachers automate everyday tasks on Google Classroom.

## Setup

1. Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Create a GCP project with the Classroom API enabled ([refer](https://developers.google.com/workspace/guides/create-project))
3. Download credentials.json for desktop applications ([refer](https://developers.google.com/workspace/guides/create-credentials))
4. Zoom - Login with your account on [https://marketplace.zoom.us/develop/create](https://marketplace.zoom.us/develop/create) and create a JWT token. Copy the API key and secret.
5. Add python dependencies - run: pip install -r requirements.txt

## Scripts

### Script 01 - [PostMaterialInDraft.py](https://github.com/Diksha-Rathi/Google-Classroom-Scripts/blob/main/Scripts/01/PostMaterialInDraft.py)

**Problem Statement** -
Once a Weekly or Periodic test completes, teachers need to create several draft posts where the evaluated answer scripts of the students are uploaded. The access is restricted to one student per folder. The schema is as below - 

* PostType : Material
* Topic : \<Test title> - Answer Scripts Evaluated
* Title : Roll No <#> - \<Name of the student>
* Description : \<description text>
* For : Individual student - Same as Title

 **How to execute script?**

Prerequisite - CSV file [ClassList.csv](https://github.com/Diksha-Rathi/Google-Classroom-Scripts/blob/main/Scripts/01/ClassList.csv) with Roll number, and Full Name of each student

Script changes - Edit the following fields:
```
COURSE = <course name> 
TOPIC = <test title> - Evaluated Answer Scripts 
DESC = <description> 
```

Execute the script (if student ids are already populated in CSV, then `student.create_csv(course_id)` can be skipped).

### Script 02 - [PostMeetingLinkInAnnouncement.py](https://github.com/Diksha-Rathi/Google-Classroom-Scripts/blob/main/Scripts/02/PostMeetingLinkInAnnouncement.py)

**Problem Statement** - 
Create Zoom link for every class and post in the announcement feed everyday as per input time table. Add announcement to the classroom with below format-

* Title - \<zoom meeting title>
* Time - \<time of the class>
* Join Zoom meeting - \<Link of the zoom meeting>
* ID - \<meeting id>
* Passcode - \<meeting passcode>

**How to execute script?**

Prerequisite - CSV file [TimeTable.json](https://github.com/Diksha-Rathi/Google-Classroom-Scripts/blob/main/Scripts/02/TimeTable.json) with class schedule updated. 

Script changes - Edit the following fields:
 ```
API_KEY = '<key>'
API_SECRET = '<secret>'
 ```

Execute the script.

## ToDo 
- [ ] Improve code reusability
- [ ] Add UI using Flask

## Contribute 
Create an issue, and let's chat!

## References
[Quickstart](https://developers.google.com/classroom/quickstart/python)\
[Google Classroom API](https://developers.google.com/classroom/reference/rest)\
[Google API Python Client](https://googleapis.github.io/google-api-python-client/docs/dyn/classroom_v1.courses.html)\
[Zoom API Reference](https://marketplace.zoom.us/docs/api-reference/introduction)
