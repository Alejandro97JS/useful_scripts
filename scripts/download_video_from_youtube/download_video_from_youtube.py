import logging, json, os
from datetime import datetime
from pytubefix import YouTube

logging.getLogger().setLevel(logging.DEBUG)

# Load configuration params:
CONFIG = {}
with open("../../config.json", mode="r", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file).get("download_video_from_youtube", {})

# ID of the video
VIDEO_ID = CONFIG.get("video_id")
# Path to the output file to be saved (or directory, without filename)
ABS_PATH_OUTPUT_FILE = CONFIG.get("abs_path_output_file")

def download_youtube_video(video_id, download_abs_path, filename = None): # Method aided by GenAI
    try:
        # Construct the YouTube URL
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Create a YouTube object
        yt = YouTube(youtube_url)
        
        # Get the highest resolution stream available
        video_stream = yt.streams.get_highest_resolution()
        
        # Download the video
        logging.debug("Downloading video...")
        if not filename: # Generate a filename:
            filename = "{}{}{}".format(
                datetime.now().strftime("%Y%m%d%H%M%S"),
                yt.title.replace(" ", "")[:12],
                video_id
            )
        else:
            # Make sure there is no extension:
            filename = os.path.splitext(filename)[0]

        video_stream.download(output_path=download_abs_path, filename=filename)
        logging.debug("Download complete!")
        return True
    
    except Exception as e:
        logging.error(f"Exception downloading video from Youtube: {e}")
        return False

def main():
    logging.debug("Execution has started...")
    logging.debug(f"Id of the video is {VIDEO_ID}")
    # 1 - Create output directory if it does not exist:
    output_dirname = os.path.dirname(ABS_PATH_OUTPUT_FILE)
    if not os.path.isdir(output_dirname):
        os.makedirs(output_dirname)
    # 2 - Download video using pytube.Youtube
    download_youtube_video(VIDEO_ID, output_dirname,
        os.path.basename(ABS_PATH_OUTPUT_FILE)) # Last argument: filename (if given)
    logging.debug("Execution ends!")

if __name__ == "__main__":
    main()
