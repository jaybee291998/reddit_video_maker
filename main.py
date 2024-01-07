from reddit_service.test import get_scripts
from reddit_service.model.entry import Entry
from reddit_service.model.script import Script

from screenshot_service.model.screenshot_model import ScreenshotModel
from screenshot_service.model.screenshot_request import ScreenshotRequest
from screenshot_service.screenshot import ScreenshotService

from voice_service.model.voice_model import VoiceModel
from voice_service.model.voice_request import VoiceRequest
from voice_service.voice import VoiceService

from video_service.model.frame import Frame
from video_service.model.video_request import VideoRequest
from video_service.video_service import VideoService
import configparser
# print(scripts)

config = configparser.ConfigParser()

config.read("settings.ini")

def script_to_screenshot_requests(script: Script) -> list[ScreenshotRequest]:
    screenshot_requests: list[ScreenshotRequest] = []
    old_id = script.submission.id
    newID = 't3_' + script.submission.id
    newID = f'//shreddit-post[@id="{newID}"]'
    script.submission.handle = newID
    screenshot_requests.append(entry_to_screenshot_request(script.submission, script.url, script.folder_name, old_id))
    for comment in script.comments:
        old_id = comment.id
        newID = 't1_' + comment.id
        newID = f'//shreddit-comment[@thingid="{newID}"]'
        comment.handle = newID
        screenshot_requests.append(entry_to_screenshot_request(comment, script.url, script.folder_name, old_id))
    return screenshot_requests

def entry_to_screenshot_request(entry: Entry, url: str, folder_name: str, id: str) -> ScreenshotRequest:
    screenshot_request: ScreenshotRequest = ScreenshotRequest()
    screenshot_request.url = url
    screenshot_request.file_name = entry.file_name
    screenshot_request.folder_name = folder_name
    screenshot_request.handle = entry.handle
    screenshot_request.id = entry.id
    return screenshot_request

def script_to_voice_requests(script: Script) -> list[VoiceRequest]:
    voice_requests: list[VoiceRequest] = []
    post_entry: Entry = script.submission
    folder_name: str = script.folder_name
    post_voice_request: VoiceRequest = entry_to_voice_request(entry=post_entry, folder_name=folder_name, use_title=True)
    voice_requests.append(post_voice_request)
    for comment in script.comments:
        comment_voice_request: VoiceRequest = entry_to_voice_request(entry=comment, folder_name=folder_name)
        voice_requests.append(comment_voice_request)
    return voice_requests

def entry_to_voice_request(entry: Entry, folder_name: str, use_title=False) -> VoiceRequest:
    voice_request: VoiceRequest = VoiceRequest()
    voice_request.file_name = entry.file_name
    voice_request.folder_name = folder_name
    voice_request.id = entry.id
    if use_title:
        voice_request.text = entry.title
    else:
        voice_request.text = entry.body
    return voice_request

def create_video_request(file_name: str, folder_name, background_video_path: str, frames: list[Frame]) -> VideoRequest:
    video_request: VideoRequest = VideoRequest(file_name=file_name, folder_name=folder_name, background_video_path=background_video_path)
    # video_request.file_name = file_name
    # video_request.folder_name = folder_name
    # video_request.background_video_path = background_video_path
    video_request.frames = frames
    return video_request

def make_frames(voice_models: list[VoiceModel], screenshot_models: list[ScreenshotModel]) -> list[Frame]:
    frames: list[Frame] = []
    voice_model_dic = {}
    for voice_model in voice_models:
        voice_model_dic[voice_model.id] = voice_model
    for screenshot_model in screenshot_models:
        frame: Frame = Frame()
        frame.id = screenshot_model.id
        frame.image_path = screenshot_model.path
        frame.audio_path = voice_model_dic[screenshot_model.id].path
        frames.append(frame)
    return frames


scripts: list[Script] = get_scripts(sub_reddit_name="AskReddit", limit=2)
screenshot_service: ScreenshotService = ScreenshotService()
voice_service: VoiceService = VoiceService()
video_service: VideoService = VideoService()
list_models_all: list[list[ScreenshotModel]] = []
list_voice_models_all: list[list[VoiceModel]] = []
background_video_path: str = config["Background"]["background_dir"] + "/test_vid.mp4"
for script in scripts:
    screenshot_requests: list[ScreenshotRequest] = script_to_screenshot_requests(script)
    list_models: list[ScreenshotModel] = screenshot_service.take_screenshots_by_ID(screenshot_requests=screenshot_requests)

    voice_requests: list[VoiceRequest] = script_to_voice_requests(script)
    list_voice_models: list[VoiceModel] = voice_service.get_voices(voice_requests)
    frames: list[Frame] = make_frames(voice_models=list_voice_models, screenshot_models=list_models)
    file_name: str = script.submission.file_name
    video_request: VideoRequest = create_video_request(file_name, script.folder_name, background_video_path, frames)
    video_model: str = video_service.create_video_clip(video_request)
    list_voice_models_all.append(list_voice_models)
# print(list_models_all)
# print(list_voice_models_all)
