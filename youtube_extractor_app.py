import streamlit as st
import os
from main import main

st.title('Youtube mp3 file extractor')
st.markdown("""
##### 유튜브 링크를 입력하면 mp3 파일을 추출해 줍니다.
""")

# 링크 입력
urls = st.text_area('Youtube 링크를 입력합니다. (Enter키를 통해 각 링크를 구분지어 입력합니다.)', )
concat = st.checkbox('출력한 음원을 합치려면 체크하세요.')

# 추출 시작 버튼
if st.button('Run Extractor'):
    url_list = urls.split()
    main(url_list, concat=concat)
    # 프로그래스 바 필요
    # 추출 완료 시 음원 디렉토리 정보 제공(리스트창) -> txt로 저장하자

# 추출이 끝나면
# 리스트창으로 음원 선택 시 해당 재생 바 제공

if os.path.isfile('audio_list.txt'):
    with open('audio_list.txt', 'r') as f:
        read_txt = f.read()
        audio_path_list = read_txt.strip().split(sep='\n')
else:
    audio_path_list = []

audio_sample = st.selectbox(
    '추출한 음원 리스트',
    audio_path_list
    )
# 샘플 오디오 플레이어
st.audio(audio_sample, format='audio/mp3')