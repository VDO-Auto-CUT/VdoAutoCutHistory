
# V-DO Auto Cut

Welcome to our first term project, V-DO Auto Cut! This project is aimed at automating the process of cutting out parts of a video that have no sound. We use Python and a script called `movie.py` for this purpose.

## Overview

V-DO Auto Cut is a tool designed to enhance video editing efficiency by automatically removing silent parts from video files. This tool can be particularly useful for content creators, streamers, and anyone looking to streamline their video editing process.

## Features

1. **Convert MP4 to MP3**: Extracts the audio from a video file.
2. **Track No-Sound Duration**: Identifies the start and end times of silent parts in the audio.
3. **Cut Video**: Removes the silent parts from the original video file and generates a new video file.

## How It Works

1. **Conversion**: The script converts the input MP4 video file to an MP3 audio file to analyze the sound.
2. **Silence Detection**: It scans the audio file to track the duration of silence, noting the start and end times.
3. **Video Cutting**: Using the timestamps from the silence detection step, it cuts the silent parts from the original video file and creates a new, trimmed video file.

## Requirements

- Python 3.x
- moviepy library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/V-DO-Auto-Cut.git
    ```
2. Navigate to the project directory:
    ```bash
    cd V-DO-Auto-Cut
    ```
3. Install the required libraries:
    ```bash
    pip install moviepy
    ```

## Usage

1. Place your MP4 file in the project directory.
2. Run the script:
    ```bash
    python movie.py your_video_file.mp4
    ```
3. The output will be a new MP4 file with silent parts removed.

## Contributors

- [Your Name](https://github.com/yourusername)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


