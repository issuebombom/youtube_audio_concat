from utils import YoutubeAudioExtractor
import os

def main(urls, user_name, concat=False):
    youtube = YoutubeAudioExtractor(urls, user_name=user_name)
    youtube.extract(concat_audio=concat)

if __name__ == '__main__':
    main()
    
