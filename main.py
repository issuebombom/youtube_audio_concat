from utils import YoutubeAudioExtractor

def main():

    url_list = [

        "https://youtu.be/YYOUHVJPukQ", 
        "https://youtu.be/xTZHYA4Asi0",
        "https://youtu.be/QM-vx1lrLaY"
        
        ] # examples
    youtube = YoutubeAudioExtractor(url_list)
    audio_path_list = youtube.extract(concat_audio=True)

    print(audio_path_list)

if __name__ == '__main__':
    main()
    
