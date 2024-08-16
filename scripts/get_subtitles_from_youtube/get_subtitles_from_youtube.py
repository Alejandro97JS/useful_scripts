import logging, json, os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

logging.getLogger().setLevel(logging.DEBUG)

# Load configuration params:
CONFIG = {}
with open("../../config.json", mode="r", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file).get("get_subtitles_from_youtube", {})

# ID of the video
VIDEO_ID = CONFIG.get("video_id")
# Path to the output file to be saved (must be txt format):
ABS_PATH_OUTPUT_FILE = CONFIG.get("abs_path_output_file")

def main():
    logging.debug("Execution has started...")
    logging.debug(f"Id of the video is {VIDEO_ID}")
    # 1 - Extract text of the subtitles of the video:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(VIDEO_ID)
    except:
        transcript = YouTubeTranscriptApi.get_transcript(VIDEO_ID, languages=("es",))
    text = TextFormatter().format_transcript(transcript)
    # 2 - Create output directory if it does not exist:
    output_dirname = os.path.dirname(ABS_PATH_OUTPUT_FILE)
    if not os.path.isdir(output_dirname):
        os.makedirs(output_dirname)
    # 3 - Save text file with subtitles:
    with open(ABS_PATH_OUTPUT_FILE, mode="w", encoding="utf-8") as f:
        f.write(text)
    logging.debug("Execution ends!")

if __name__ == "__main__":
    main()
