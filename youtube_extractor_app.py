import streamlit as st
import datetime as dt
import time
import os
from utils import YoutubeAudioExtractor, audio_player, get_audio_list, get_audio_length, rename_audio, delete_audio, trim_audio, fade_audio

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

# 한 번이라도 추출을 해야 userdata에 사용자 폴더가 생성됨
user_dir = os.path.join('userdata', user_name)
if os.path.exists(user_dir):
    audio_txt_path = get_audio_list(user_dir) # refresh audio list

    with open(audio_txt_path, 'r') as txt:
        read_txt = txt.read()
        audio_list = read_txt.strip().split(sep='\n')

        st.markdown("""## """) # empty space for layer

        # 음원 리스트 보기
        col1, col2 = st.columns([8, 1.4])
        with col1:
            selected_audio_name = st.selectbox("저장된 음원 목록", audio_list, label_visibility='collapsed')
        with col2:
            if st.button('Refresh'):
                get_audio_list(user_dir)
        
        # metadata
        audio_name = selected_audio_name
        audio_path = os.path.join(user_dir, audio_name)
        audio_length = get_audio_length(audio_path)

        # 플레이어 및 다운로드 기능 생성
        audio_player(user_dir, audio_path, audio_name, 1)

    st.markdown("""# """) # empty space for layer
    st.markdown("""# """) # empty space for layer
    
    with st.expander('음원 편집'):
        tab1, tab2, tab3, tab4 = st.tabs(['이름 변경', '음원 합치기', '음원 삭제', '음원 편집'])

        with tab1:
            # 오디오 파일 이름 수정
            st.markdown(f'현재 선택된 파일은 :red[{audio_name}] 입니다.')
            col1, col2 = st.columns(2)
            with col1:
                switch_name = st.text_input('수정할 파일명을 적어주세요. ex) fixed_audio', label_visibility='collapsed')
            with col2:
                if st.button('Rename'):
                    rename_audio(user_dir, audio_path, audio_name, switch_name)
        with tab2:
            # NOTE: multiselect에서 중복 선택도 가능하도록 수정하면 좋겠음
            concat_list = st.multiselect('합칠 음원을 순서대로 선택하세요.', audio_list)
            file_name = st.text_input(label="저장할 파일명을 정해주세요.", 
                                    value="audio_output")
            file_name += ".mp3"
            # normalize = st.checkbox('Normalize')
            if st.button('Concatenate'):
                concat_audio_path = youtube.concat_mp3_file(concat_list, file_name)

                # 플레이어 및 다운로드 기능 생성
                audio_player(user_dir, concat_audio_path, file_name, 2)
        with tab3:
            st.markdown(f'현재 선택된 파일은 :red[{audio_name}] 입니다.')
            if st.button('Delete'):
                delete_audio(audio_path)

        with tab4:
            temp_audio_path = os.path.join(user_dir, '[Temp]audio.mp3')
            trim_audio_path = os.path.join(user_dir, '[Trim]'+audio_name)
            time_range = [str(dt.timedelta(seconds=seconds)) for seconds in range(audio_length+1)] # 0:00:00 형태로 출력
    
            # 최소 최대 시간 값 선택 바
            start_sec, end_sec = st.select_slider('편집 범위를 선택해주세요',
                                                options=time_range,
                                                value=(time_range[0], time_range[-1])
                                                )
            st.markdown(f"You seleted length between :red[{start_sec}] and :red[{end_sec}]")
            
            if st.button('Trim'):
                if os.path.exists(temp_audio_path): # 임시파일이 있을 경우 우선 삭제합니다.
                    os.popen(f"rm '{temp_audio_path}'").read()

                # 편집된 파일을 임시파일명으로 저장합니다.
                trim_audio(audio_path, start_sec, end_sec, temp_audio_path)

                while True: # Trim이 완료될 때 까지 대기
                    if os.path.exists(temp_audio_path):
                        temp_audio_length = get_audio_length(temp_audio_path)
                        break
                    time.sleep(0.5)
                # 임시파일 음원 양 끝단에 fade in/out처리 후 최종 저장합니다.
                fade_audio(temp_audio_path, temp_audio_length, trim_audio_path, fade_type='edge', duration=0.05)
