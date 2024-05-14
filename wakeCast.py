import sys
import time
import pychromecast
import typer
from pychromecast.controllers import youtube
import re


# Define colors for formatting
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Default YouTube video ID
DEFAULT_YOUTUBE_VIDEO_ID = "PWn-Wh9O3N8"

# Banner
BANNER = f"""
{bcolors.BOLD}                                                  Made by @tzero86
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
    print(f"{bcolors.OKBLUE}[..] WakeCast is looking for Online Chromecast devices on the network...{bcolors.ENDC}")
    chromecasts, _ = pychromecast.get_chromecasts()
    if not chromecasts:
        print(f"{bcolors.FAIL}[x.x] Sorry I was unable to find any Chromecast devices on the network. Make sure you "
              f"are connected to the same network as the Chromecast device.{bcolors.ENDC}")
        sys.exit(1)
    print(
        f"{bcolors.OKGREEN}[..] A total of {len(chromecasts)} Chromecast devices were found active on the network.{bcolors.ENDC}")
    # Display available devices for selection
    for i, cc in enumerate(chromecasts):
        print(f"[{i}] {cc.name}")
    print(
        f"{bcolors.OKBLUE}[-.-] Please specify a Chromecast device you want to compensate the lack of functionality "
        f"for (Enter its Index, e.g. 1):{bcolors.ENDC}")
    while True:
        try:
            index = int(input())
            if index < 0 or index >= len(chromecasts):
                raise ValueError
            break
        except ValueError:
            print(f"{bcolors.FAIL}[x.x] ERROR: Invalid device index number. Please Try again:{bcolors.ENDC}")
    return chromecasts[index]


def play_youtube_video(chromecast_device: pychromecast.Chromecast, video_id: str, wait_time: int):
    try:
        print(
            f"{bcolors.OKBLUE}[..] WakeCast is connecting to Chromecast device now. '{chromecast_device.name}'...{bcolors.ENDC}")
        chromecast_device.wait()
        print(f"{bcolors.OKGREEN}[..] WakeCast is Connected to '{chromecast_device.name}.'.{bcolors.ENDC}")
        print(
            f"{bcolors.OKBLUE}[..] Now we'll wait for {wait_time} seconds before WakeCast plays the video...{bcolors.ENDC}")
        time.sleep(wait_time)
        print(f"{bcolors.OKBLUE}[..] Ok we are playing the YouTube video with ID '{video_id}'.{bcolors.ENDC}")
        yt = pychromecast.controllers.youtube.YouTubeController()
        chromecast_device.register_handler(yt)
        yt.play_video(video_id)
    except Exception as e:
        print(
            f"{bcolors.FAIL}[x.x] Well... Something went south I think... Let's try again from the top, shall we?: {e}{bcolors.ENDC}")
        sys.exit(1)


def extract_video_id(url: str) -> str:
    # Regular expressions to extract video ID from YouTube URLs
    patterns = [
        r'^(?:http|https)://(?:www\.)?youtube\.com/watch\?v=([0-9A-Za-z_-]{11})',
        r'^(?:http|https)://youtu.be/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"[x.x] As per our top engineering ferrets team, this is not a valid YouTube video URL we can use.\n"
                     f"The high council recommends trying a different one and start again: {url}\n[..] I think I'll "
                     f"close myself now. See you next time!")


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
                raise ValueError(f"[x.x] The Device '{device}' was not found, Did you type the name correctly?.")
        except Exception as e:
            print(f"{bcolors.WARNING}[0.0] Warning: Something failed when trying to use the device {chromecast_device} "
                  f"We need to try manual selection instead...{e}{bcolors.ENDC}")

    if not chromecast_device:
        chromecast_device = choose_device()

    video_id = DEFAULT_YOUTUBE_VIDEO_ID
    if video:
        try:
            video_id = extract_video_id(video)
        except ValueError as e:
            print(f"{bcolors.FAIL}{e}{bcolors.ENDC}")
            sys.exit(1)

    play_youtube_video(chromecast_device, video_id, wait_time)

    print(f"{bcolors.OKGREEN}[..] All Done, shutting down WakeCast.{bcolors.ENDC}")


if __name__ == "__main__":
    app()

