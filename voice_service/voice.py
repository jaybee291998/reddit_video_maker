import os

import pyttsx3
import configparser

from .model.voice_request import VoiceRequest
from .model.voice_model import VoiceModel

class VoiceService:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        self.voice_path: str = config['VoiceService']['voice_dir']
        rate: int = int(config['VoiceService']['pyttsx_rate'])
        volume: float = float(config['VoiceService']['pyttsx_volume'])
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def get_voice(self, voice_request: VoiceRequest) -> VoiceModel:
        file_name = voice_request.file_name
        folder_name = voice_request.folder_name
        base_path: str = f'{self.voice_path}/{folder_name}'
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        full_path = f'{base_path}/{file_name}.wav'

        print(full_path)
        self.engine.save_to_file(voice_request.text, full_path)

        voice_model: VoiceModel = VoiceModel()

        self.engine.runAndWait()

        voice_model.id = voice_request.id
        voice_model.path = full_path
        return voice_model

    def get_voices(self, voice_requests: list[VoiceRequest]) -> list[VoiceModel]:
        voice_models: list[VoiceModel] = []
        for voice_request in voice_requests:
            voice_model: VoiceModel = self.get_voice(voice_request=voice_request)
            voice_models.append(voice_model)
        return voice_models
