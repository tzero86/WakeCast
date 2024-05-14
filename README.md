# WakeCast

![](https://i.imgur.com/ovQUUrG.png "WakeCast Ascii logo")
WakeCast is a Python script that allows you to set up a video alarm on your Chromecast device using YouTube. It fills the gap for the lack of a native alarm feature on Chromecast devices.

## Features

- Set a specific time to trigger the alarm (in seconds).
- Play a custom YouTube video URL or use the default one.
- Select the Chromecast device to play the alarm on.

## Installation

1. Clone this repository to your local machine:
````git clone https://github.com/your_username/WakeCast.git````

2. Navigate to the project directory:

````cd WakeCast````
3. Install the required packages:

````pip install -r requirements.txt````



## Usage

To use WakeCast, run the `wakeCast.py` script with the desired options:

- `--wait-time`: The time to wait before triggering the alarm.
- `--video`: (optional): The URL of the YouTube video to play. If not provided, the default video will be played (Regular Phone Alarm Sound).
- `--device` (optional): The name of the Chromecast device to play the alarm on. If not provided, WakeCast will search for available devices and prompt you to select one.

Example:

````python wakeCast.py --wait-time 60 --video https://www.youtube.com/watch?v=6JYIGclVQdw --device "Living Room"````



## Contributing

Contributions are welcome! If you have any suggestions, bug fixes, or enhancements, feel free to open an issue or submit a pull request.

