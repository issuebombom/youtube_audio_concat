import streamlit as st
import os
from utils import YoutubeAudioExtractor, player_and_download

st.title('Youtube mp3 file extractor')
st.markdown("""##### 유튜브 링크를 입력하면 mp3 파일을 추출합니다.""")

user_name = st.text_input(label='사용자 이름 입력', 
                          max_chars=20
                          )

if len(user_name) == 0:
    st.info('사용자 이름을 입력해 주세요.', icon="ℹ️")
    st.stop()

st.markdown("""##### """) # empty space for layer

# 링크 입력
urls = st.text_area('링크를 입력합니다. (여러 개 입력 시 각 링크마다 엔터키를 눌러 줄바꿈 해주세요.)', )
youtube = YoutubeAudioExtractor(urls, user_name)

# 추출 시작 버튼
if st.button('Extract', disabled=False if len(urls) != 0 else True):
    youtube.extract()

user_dir = os.path.join('userdata', user_name)
audio_txt_path = os.path.join(user_dir, 'audio_list.txt')

if os.path.exists(audio_txt_path):
    with open(audio_txt_path, 'r') as txt:
        read_txt = txt.read()
        audio_list = read_txt.strip().split(sep='\n')

        st.markdown("""## """) # empty space for layer

        # 추출한 음원 리스트 보기
        audio_name = st.selectbox("저장된 음원 목록", audio_list)
        audio_path = os.path.join(user_dir, audio_name)

        # 플레이어 및 다운로드 기능 생성
        player_and_download(user_dir, audio_path, audio_name)

    st.markdown("""# """) # empty space for layer
    st.markdown("""# """) # empty space for layer
    
    with st.expander("음원 합치기"):
        
        # NOTE: multiselect에서 중복 선택도 가능하도록 수정하면 좋겠음
        concat_list = st.multiselect('합칠 음원을 순서대로 선택하세요.', audio_list)
        file_name = st.text_input(label="저장할 파일명을 정해주세요.", 
                                value="audio_output")
        file_name += ".mp3"
        # normalize = st.checkbox('Normalize')
        if st.button('Concatenate'):
            concat_audio_path = youtube.concat_mp3_file(concat_list, file_name)

            # 플레이어 및 다운로드 기능 생성
            player_and_download(user_dir, concat_audio_path, file_name)
