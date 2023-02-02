import streamlit as st
import os
from main import main

st.title('Youtube mp3 file extractor')
st.markdown("""
##### 유튜브 링크를 입력하면 mp3 파일을 추출해 줍니다.
""")

user_name = st.text_input(label='나만의 보관할 폴더명을 지정해주세요. 이미 존재할 경우 로딩합니다.', 
                            max_chars=20,
                            type="password")

# 링크 입력
urls = st.text_area('Youtube 링크를 입력합니다. (Enter키를 통해 각 링크를 구분지어 입력합니다.)', )
concat = st.checkbox('출력한 음원을 합치려면 체크하세요.')

# 추출 시작 버튼
if st.button('Run Extractor'):
    main(urls=urls, user_name=user_name, concat=concat)

audio_list_path = os.path.join('userdata', user_name, 'audio_list.txt')
if os.path.exists(audio_list_path):
    with open(audio_list_path, 'r') as f:
        read_txt = f.read()
        audio_list = read_txt.strip().split(sep='\n')
        # 추출한 음원 리스트 보기
        audio_name = st.selectbox("보유 중인 음원 리스트", audio_list)
        audio_path = os.path.join('userdata', user_name, audio_name)
        st.audio(audio_path, format='audio/mp3') # 샘플 오디오 플레이어

        # 오디오 다운로드
        with open(audio_path, "rb") as file:
            st.download_button(label='Download selected audio file', 
                            mime='audio/mp3',
                            data=file, 
                            file_name=audio_name, 
                            )