import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from sqlalchemy.orm import Session

from app.database.models import Post

CLIENT_SECRETS_FILE = os.path.join(os.getcwd() + '/app/api/client_secret.json')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.force-ssl']


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return build('youtube', 'v3', credentials=credentials)


def get_youtube():
    yt = get_authenticated_service()
    return yt


def upload_video(title: str, description: str, model: Post, sess: Session, video_path: str):
    youtube = get_youtube()
    request_body = {
        'snippet': {
            'title': title,
            'description': description
        },
        'status': {
            'privacyStatus': 'public'  # You can set privacy status here
        }
    }

    media = MediaFileUpload(video_path)

    response = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    ).execute()
    # Video uploaded successfully!
    link = f'https://youtu.be/{response['id']}'
    model.video_youtube = link
    sess.add(model)
    sess.commit()
    return link


def delete_video(id_video):
    youtube = get_youtube()
    youtube.videos().delete(id=id_video).execute()
    # Video delete successfully!

