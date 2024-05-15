import sys
import time
import re
import pychromecast
import typer
from pychromecast.controllers import youtube


# Define colors for formatting
class bcolors:
    HEADER = '\033[95m'  # Pink
    OKBLUE = '\033[94m'  # Blue
    OKCYAN = '\033[96m'  # Cyan
    OKGREEN = '\033[92m'  # Green
    WARNING = '\033[93m'  # Yellow
    FAIL = '\033[91m'  # Red
    ENDC = '\033[0m'  # Reset color
    BOLD = '\033[1m'  # Bold
    UNDERLINE = '\033[4m'  # Underline


# Default YouTube video ID
DEFAULT_YOUTUBE_VIDEO_ID = "PWn-Wh9O3N8"

# Banner
BANNER = f"""
    {bcolors.BOLD}                                          Made by @tzero86
    ██     ██  █████  ██   ██ ███████  ██████  █████  ███████ ████████ 
    ██     ██ ██   ██ ██  ██  ██      ██      ██   ██ ██         ██    
    ██  █  ██ ███████ █████   █████   ██      ███████ ███████    ██    
    ██ ███ ██ ██   ██ ██  ██  ██      ██      ██   ██      ██    ██    
     ███ ███  ██   ██ ██   ██ ███████  ██████ ██   ██ ███████    ██ 

    A Chromecast Video-alarm using YouTube app, apparently expecting 
    a native alarm app is too much for a Chromecast device these days...                                                  
"""

app = typer.Typer()


def choose_device() -> pychromecast.Chromecast:
    print(f"{bcolors.OKBLUE}[INF] WakeCast is looking for Online Chromecast devices on the network...{bcolors.ENDC}")
    chromecasts, _ = pychromecast.get_chromecasts()
    if not chromecasts:
        print(f"{bcolors.FAIL}[ERR] Sorry I was unable to find any Chromecast devices on the network. Make sure you "
              f"are connected to the same network as the Chromecast device.{bcolors.ENDC}")
        sys.exit(1)
    print(
        f"{bcolors.OKGREEN}[INF] A total of {len(chromecasts)} Chromecast devices were found active on the network.{bcolors.ENDC}")
    # Display available devices for selection
    for i, cc in enumerate(chromecasts):
        print(f"[{i}] {cc.name}")
    print(
        f"{bcolors.OKBLUE}[INP] Please specify the Chromecast device you want to compensate the lack of functionality "
        f"for (Enter its Index, e.g. 1):{bcolors.ENDC}")
    while True:
        try:
            index = int(input())
            if index < 0 or index >= len(chromecasts):
                raise ValueError
            break
        except ValueError:
            print(f"{bcolors.FAIL}[ERR] ERROR: Invalid device index number. Please Try again:{bcolors.ENDC}")
    return chromecasts[index]


def play_youtube_video(chromecast_device: pychromecast.Chromecast, video_id: str, wait_time: int):
    try:
        print(
            f"{bcolors.OKBLUE}[INF] WakeCast is connecting to Chromecast device now. '{chromecast_device.name}'...{bcolors.ENDC}")
        chromecast_device.wait()
        print(f"{bcolors.OKGREEN}[INF] WakeCast is Connected to '{chromecast_device.name}.'.{bcolors.ENDC}")

        for remaining in range(wait_time, 0, -1):
            sys.stdout.write(f"\r{bcolors.OKBLUE}[INF] Let's wait a bit for that timer to go off: {remaining} seconds "
                             f"remaining...{bcolors.ENDC}")
            sys.stdout.flush()
            time.sleep(1)
        print(f"\r{bcolors.OKGREEN}[INF] The wait is over. Starting video...{bcolors.ENDC}")

        print(f"{bcolors.OKBLUE}[INF] Ok we are playing the YouTube video with ID '{video_id}'.{bcolors.ENDC}")
        yt = pychromecast.controllers.youtube.YouTubeController()
        chromecast_device.register_handler(yt)
        yt.play_video(video_id)
    except Exception as e:
        print(
            f"{bcolors.FAIL}[ERR] Well... Something went south. Let's try that again from the top, shall we?: {e}{bcolors.ENDC}")
        sys.exit(1)


def is_valid_youtube_url(url: str) -> bool:
    # Regular expression to validate YouTube URL
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    return bool(re.match(pattern, url))


def extract_video_id(url: str) -> str:
    # Regular expression to extract video ID from YouTube URL
    video_id_match = re.search(
        r'(?:v=|youtu\.be/|/embed/|/v/|/e/|/watch\?v=|/watch\?v%3D|/watch\?.+&v=)([^#\&\?]{11})', url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError(
            f"{bcolors.FAIL}[ERR] As per our top engineering ferrets team, {url} is not a valid YouTube video URL we can use.\n The "
            f"high council recommends trying a different one.{bcolors.ENDC}")



@app.command()
def main(wait_time: int = typer.Option(..., help="The time to wait before triggering the alarm (in seconds)"),
         video: str = typer.Option(None, "--video", "-v", help="The YouTube video URL to play"),
         device: str = typer.Option(None, "--device", "-d", help="The Chromecast device name")):
    print(BANNER)  # Print the banner when the script starts

    chromecast_device = None

    if device:
        try:
            chromecast_device = next(cc for cc in pychromecast.get_chromecasts()[0] if cc.name == device)
            if not chromecast_device:
                raise ValueError(
                    f"{bcolors.FAIL}[ERR] The Device '{device}' was not found, Did you type the name correctly?.{bcolors.ENDC}")
        except Exception as e:
            print(
                f"{bcolors.WARNING}[WARN] Warning: Something failed when trying to use the device {device}. We need to try manual selection instead...{e}{bcolors.ENDC}")

    if not chromecast_device:
        chromecast_device = choose_device()

    video_id = DEFAULT_YOUTUBE_VIDEO_ID
    if video:
        while True:
            if is_valid_youtube_url(video):
                try:
                    video_id = extract_video_id(video)
                    print(f"{bcolors.OKGREEN}[INF] Extracted video ID: {video_id}{bcolors.ENDC}")
                    break
                except ValueError as e:
                    print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")
            else:
                print(f"{bcolors.FAIL}[ERR] The provided URL '{video}' is not a valid YouTube URL.{bcolors.ENDC}")

            video = input(
                f"{bcolors.OKBLUE}[INP] Please enter a valid YouTube video URL or type 'default' to use the default video:{bcolors.ENDC} ")
            if video.lower() == 'default':
                video_id = DEFAULT_YOUTUBE_VIDEO_ID
                break

    play_youtube_video(chromecast_device, video_id, wait_time)

    print(f"{bcolors.OKGREEN}[INF] All Done, shutting down WakeCast.{bcolors.ENDC}")


if __name__ == "__main__":
    app()
