import os
from pytube import YouTube
from tqdm import tqdm
import re
import streamlit as st

class YoutubeAudioExtractor:
    """Youtube 링크를 리스트 형식으로 받으면 해당 링크에서 음원 추출

    Args:
        url_list (list): Youtube 링크를 리스트로 입력
        user_dir (str, optional): 추출한 음원 파일 저장 디렉토리명 지정. Defaults to './audio_cache'
    """

    def __init__(self, urls, user_name):
        self.user_dir = os.path.join("userdata", user_name)
        self.url_list = re.findall('http[a-zA-Z0-9:/.?=_\-]+', urls)

    def extract(self):
        """Youtube 음원 추출 및 폴더 내 음원 목록 저장
        """
        if not os.path.exists(self.user_dir): # 지정한 디렉토리가 없을 경우 신규 생성
            os.popen(f"mkdir -p {self.user_dir}")

        self.get_mp3_from_youtube()
        # 저장된 음원 목록 txt파일로 저장
        os.popen(f"ls {self.user_dir} | grep -E '.mp3' > {os.path.join(self.user_dir, 'audio_list.txt')}").read()
        
    def get_mp3_from_youtube(self):
        """입력된 유튜브 url에서 mp4 확장자를 가지는 음원을 추출하여 지정한 디렉토리에 저장합니다.
        pytube docs: https://pytube.io/en/latest/_modules/pytube/streams.html#Stream.download
        """
        my_bar = st.progress(0)
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
            
            my_bar.progress((i+1) * 100//len(self.url_list)) # 프로그래스 바

    def concat_mp3_file(self, concat_list, file_name):
        """여러 mp3 파일을 concat합니다.
        """

        concat_dir = os.path.join(self.user_dir, 'concat_cache') # concat 폴더 경로 지정

        if not os.path.exists(concat_dir): # 지정한 디렉토리가 없을 경우 신규 생성
            os.popen(f"mkdir -p {concat_dir}").read()
        
        else: # 기존 폴더 삭제 후 재생성
            os.popen(f"rm -rf {concat_dir} && mkdir -p {concat_dir}").read()

        concat_audio_path = os.path.join(concat_dir, file_name)
        concat_list_txt = os.path.join(self.user_dir, 'concat_list.txt') # concat 파일의 경로
        
        with open(concat_list_txt, 'w') as txt: # concat용 command text 작성
            for name in concat_list:
                txt.write(f"""file '{name}'\n""")

        os.popen(f"""
                    ffmpeg -f concat -safe 0 -i {concat_list_txt} -c copy {concat_audio_path} &&
                    rm -f {concat_list_txt}
                """).read()
        
        # NOTE: normalize 구현 고민
        """normalize cmd
        ffmpeg-normalize {} -o {} -f -v \
        -c:a libmp3lame --normalization-type ebu --target-level -14 \
        --keep-loudness-range-target &&
        """
        return concat_audio_path

def player_and_download(user_dir, file_path, file_name):
    # 샘플 오디오 플레이어
    st.audio(file_path, format='audio/mp3')

    # 오디오 다운로드 버튼
    with open(file_path, "rb") as file:
        st.download_button(label='Download', mime='audio/mp3', data=file, file_name=file_name)
    
    # NOTE: 압축 후 다운로드 기능 구현 고민 (st.download버튼을 직접 클릭 외 실행하는 방법을 찾아야 함)
    '''
    if user_dir is not None:

        st.button(on_click=zip_and_download)

        def zip_and_download(user_dir):

            os.popen(f"""zip audio.zip {user_dir}/*.mp3""").read() # 압축

            zipfile_path = os.path.join(user_dir, 'audio.zip') # 압축파일 경로
            with st.spinner('Wait for zip...'): # 압축파일 생성 전까지 대기
                while True:
                    if os.path.exists(zipfile_path):
                        break
                    time.sleep(0.5)

            with open(zipfile_path, "rb") as zipfile:
                st.download_button(label='Download all', data=zipfile, file_name='audio.zip')
    '''

