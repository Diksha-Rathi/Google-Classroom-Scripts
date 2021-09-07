from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from tempfile import NamedTemporaryFile

import shutil
import os.path
import csv
import json

class Authentication():
    def get_token(self, scopes):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

class Course(object):
    def __init__(self, service):
        self.service = service.courses()

    def list(self):
        service = self.service
        response = service.list().execute()
        courses = response.get('courses', [])
        return courses

    def get_course_by_name(self, name):
        courses = self.list()
        result = next((course for course in courses if course['name'].lower() == name), None)
        if result == None:
            raise Exception('Course does not exist.')
        else:
            return result['id']

class Student(object):
    def __init__(self, service):
        self.service = service.courses().students()

    def list(self, course_id):
        service = self.service
        students = []
        page_token = None

        while True:
            response = service.list(courseId=course_id,pageToken=page_token,
                                              pageSize=20).execute()
            students.extend(response.get('students', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break
        return students

    def create_csv(self, course_id):
        students = self.list(course_id)

        # create dict with full name as key to get O(1) access time
        records = {}
        for student in students:
            records[student['profile']['name']['fullName']] = student['userId']

        fields = ['RollNo', 'Name', 'StudentId']
        
        filename = 'ClassList.csv'
        tempfile = NamedTemporaryFile(mode='w', delete=False)

        with open(filename, 'r') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            writer = csv.DictWriter(tempfile, fieldnames=fields)
            # skip header
            next(reader)
            for row in reader:
                row['StudentId'] = records[row['Name']]
                row = {'RollNo': row['RollNo'], 'Name': row['Name'], 'StudentId': row['StudentId']}
                writer.writerow(row)

        shutil.move(tempfile.name, filename)

class Topic(object):
    def __init__(self, service):
        self.service = service.courses().topics()

    def list(self, course_id):
        service = self.service
        results = service.list(courseId=course_id).execute() 
        topics = results.get('topic',[])
        return topics

    def create(self, course_id, name):
        topics = self.list(course_id)
        exists = next((topic for topic in topics if topic['name'].lower() == name.lower()), None)
        if exists == None:
            service = self.service
            response = service.create(courseId=course_id,body={'name': name}).execute()
            return response['topicId']
        else:
            return exists['topicId']
    
class CourseWork(object):
    def __init__(self, service):
        self.service = service.courses().courseWorkMaterials()

    def post_material(self, course_id, topic_id, description):
        with open('ClassList.csv', newline='') as f:
            reader = csv.reader(f)
            students = list(reader)

        for student in students:
            title = 'Roll No.' + student[0] + ' - ' + student[1]
            request = {
              'courseId': course_id,
              'topicId': topic_id,
              'title': title,
              'description': description,
              'state': 'DRAFT',
              'assigneeMode': 'INDIVIDUAL_STUDENTS',
              'individualStudentsOptions': {
                    'studentIds': [
                      student[2]
                    ]
                }
            }
            self.create(course_id, request)

    def create(self, course_id, request):
        service = self.service
        request = service.create(courseId=course_id, body=request).execute()

def main():
    # Update below fields
    COURSE = '<course name>'
    TOPIC = '<test title> - Evaluated Answer Scripts'
    DESC = '<description>'

    scopes = ['https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters.readonly',
    'https://www.googleapis.com/auth/classroom.courseworkmaterials',
    'https://www.googleapis.com/auth/classroom.topics']

    authObj = Authentication()
    creds = authObj.get_token(scopes)

    if (creds == None):
        print('Credentials not generated.')
    else: 
        service = build('classroom', 'v1', credentials=creds)
        course = Course(service)
        topic = Topic(service)
        student = Student(service)
        course_work = CourseWork(service)

        course_id = course.get_course_by_name(COURSE.lower())
        topic_id = topic.create(course_id, TOPIC)

        # One time - populate csv with student ids
        student.create_csv(course_id)

        # post material for students with individual access rights in draft
        course_work.post_material(course_id, topic_id, DESC)

if __name__ == '__main__':
    main()