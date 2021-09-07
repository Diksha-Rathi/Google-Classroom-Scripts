from time import time
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import jwt
import requests
import json
import os

class Zoom():
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def get_token(self):
        return jwt.encode(
                {'iss': self.key, 'exp': time() + 5000},
                self.secret,
                algorithm='HS256'
            )

    def create_meeting_obj(self, topic, meeting_type, time):
        return {
            'topic': topic,
            'type': meeting_type,
            'start_time': time,
            'duration': '45',
            'timezone': 'Asia/Kolkata',
            'settings': {
                'host_video': False,
                'participant_video': True,
                'in_meeting': True,
                'join_before_host': False,
                'waiting_room': True,
                'mute_upon_entry': True,
                'audio': 'voip',
                'allow_multiple_devices': True
            },
            'pre_schedule': False
        }

    def schedule_meeting(self, data):
        headers = {
            'authorization': 'Bearer %s' % self.get_token(),
            'content-type': 'application/json'
        }

        response = requests.post(
            f'https://api.zoom.us/v2/users/me/meetings', 
            headers=headers, data=json.dumps(data))

        meeting = json.loads(response.text)

        return data['start_time'], meeting['join_url'], str(meeting['id']), meeting['password']
            
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

class Course():
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

class Announcement():
    def __init__(self, service):
        self.service = service.courses().announcements()

    def create(self, course_id, text):
        service = self.service
        request = {
              'courseId': course_id,
              'text': text,
              'state': 'PUBLISHED',
              'assigneeMode': 'ALL_STUDENTS'
            }
        response = service.create(courseId=course_id, body=request).execute()

def main():
    # Update API key and secret
    API_KEY = '<key>'
    API_SECRET = '<secret>'

    scopes = ['https://www.googleapis.com/auth/classroom.announcements',
    'https://www.googleapis.com/auth/classroom.courses.readonly']

    zoomObj = Zoom(API_KEY, API_SECRET);
    authObj = Authentication()

    creds = authObj.get_token(scopes)

    if (creds == None):
        print('Credentials not generated.')
    else: 
        service = build('classroom', 'v1', credentials=creds)
        courseObj = Course(service)
        announcementObj = Announcement(service)

        # read json file
        f = open('TimeTable.json',)
        timetable = json.load(f)
        f.close()
        
        # loop for each json object and post an announcement in Google Classroom      
        for item in timetable:
            meetings = []
            course = item['course']
            title = item['meeting_title']

            if len(item['meeting_time']) > 0:
                for meeting_time in item['meeting_time']:
                    meeting_obj = zoomObj.create_meeting_obj(title, 2, meeting_time)
                    meetings.append(zoomObj.schedule_meeting(meeting_obj))

                # Post in classroom
                course_id = courseObj.get_course_by_name(course.lower())
                text = 'Title : ' + title + '\n'
                for meeting in meetings:
                    # Update date format
                    date_obj = datetime.strptime(meeting[0], "%Y-%m-%dT%H:%M:%S")
                    date_str = datetime.strftime(date_obj, "%d %b, %Y %-I:%M %p")

                    text = text + '\n' + ('Time : ' + date_str + '\n'
                        + 'Join Zoom meeting : ' + meeting[1] + '\n'
                        + 'ID : ' + meeting[2] + '\n'
                        + 'Passcode : ' + meeting[3] + '\n')

                announcementObj.create(course_id, text)
            
if __name__ == '__main__':
    main()