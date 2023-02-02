import os
from pytube import YouTube
from tqdm import tqdm
import re

class YoutubeAudioExtractor:
    """Youtube 링크를 리스트 형식으로 받으면 해당 링크에서 음원 추출

    Args:
        url_list (list): Youtube 링크를 리스트로 입력
        user_dir (str, optional): 추출한 음원 파일 저장 디렉토리명 지정. Defaults to './audio_cache'
    """

    def __init__(self, urls, user_name):
        user_dir = os.path.join("userdata", user_name)
        if not os.path.isdir(user_dir): # 지정한 디렉토리가 없을 경우 신규 생성
            os.popen(f"mkdir -p {user_dir}")

        self.url_list = urls.split()
        self.user_dir = user_dir

    def extract(self, concat_audio=False):
        """Youtube 음원 추출 및 합치기

        Args:
            concat_audio (bool, optional): True 선택 시 추출된 mp3 파일을 하나로 합친다. Defaults to False.
        """

        self.get_mp3_from_youtube()

        if concat_audio:
            self.concat_mp3_file()

        # 저장된 음원 목록 txt파일로 저장
        os.popen(f"ls {self.user_dir} | grep -E '.mp3' > {os.path.join(self.user_dir, 'audio_list.txt')}").read()
        
    def get_mp3_from_youtube(self):
        """입력된 유튜브 url에서 mp4 확장자를 가지는 음원을 추출하여 지정한 디렉토리에 저장합니다.
        pytube docs: https://pytube.io/en/latest/_modules/pytube/streams.html#Stream.download
        """

        for i, url in enumerate(tqdm(self.url_list)):

            youtube = YouTube(url)
            condition = youtube.streams.filter(only_audio=True, file_extension='mp4', type='audio', abr='128kbps').order_by('abr').last()
            condition.download(output_path=self.user_dir, filename='extract_file.mp4') # 다운로드가 완료되면 다음 line을 실행하는 것 확인

            # convert mp4a to mp3
            title = re.sub('[^가-힣A-Za-z0-9\s]', '', youtube.title).strip() # 특수문자 제외
            title = re.sub(' ', '\\ ', title) # 한글 띄어쓰기 앞에 \ 넣기
            save_file_path = os.path.join(self.user_dir, 'extract_file.mp4')
            converted_file_path = os.path.join(self.user_dir, title + '.mp3')

            os.popen(f"""
                    ffmpeg -i {save_file_path} {converted_file_path} -y &&
                    rm -f {save_file_path}
                    """).read() 

    def concat_mp3_file(self):
        """여러 mp3 파일을 concat합니다.
        """

        os.popen(f"""
                    printf "file '%s'\n" {self.user_dir}/*.mp3 > .concat_list.txt &&
                    ffmpeg -f concat -safe 0 -i .concat_list.txt -c copy {self.user_dir}/concat_output.mp3 &&
                    rm -f .concat_list.txt
                """).read()
