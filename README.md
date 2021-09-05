# Google-Classroom-Scripts
A collection of Python scripts to help school teachers automate everyday tasks on Google Classroom.

## Setup

1. Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Create a GCP project with the Classroom API enabled (refer)[https://developers.google.com/workspace/guides/create-project].
3. Download credentials.json for desktop applications (refer)[https://developers.google.com/workspace/guides/create-credentials].
4. Add python dependencies - run: pip install -r requirements.txt

## Scripts

### Script 01 - [PostMaterialInDraft.py](https://github.com/Diksha-Rathi/Google-Classroom-Scripts/blob/main/Scripts/PostMaterialInDraft.py)

**Problem Statement** -
Once a Weekly or Periodic test completes, teachers need to create several draft posts where the evaluated answer scripts of the students are uploaded. The access is restricted to one student per folder. The schema is as below - 

* PostType : Material
* Topic : \<Test title> - Answer Scripts Evaluated
* Title : Roll No <#> - \<Name of the student>
* Description : \<description text>
* For : Individual student - Same as Title

**How to execute script?**
  
Prerequisite - CSV file with Roll number, and Full Name of each student

Script changes - Edit the following fields:
```
COURSE = <course name> 
TOPIC = <test title> - Evaluated Answer Scripts 
DESC = <description> 
```

Execute the script (if student ids are already populated in CSV, then `student.create_csv(course_id)` can be skipped).

### Script 02 - PostMeetingLinkInAnnouncement.py

**Problem Statement** - 
Create Zoom link for every class and post in the announcement feed everyday as per input time table.

**How to execute script?**

\<WIP>

## ToDo 
- [ ] Improve code reusability
- [ ] Add UI using Flask

## Contribute 
Create an issue, and let's chat!

## References
(Quickstart)[https://developers.google.com/classroom/quickstart/python]
(Google Classroom API)[https://developers.google.com/classroom/reference/rest]
(Google API Python Client)[https://googleapis.github.io/google-api-python-client/docs/dyn/classroom_v1.courses.html]