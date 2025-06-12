# Reddit Media Downloader

Reddit Media Downloader is a Python script that allows you to download all media (images, GIFs, and videos) posted by a specific Reddit user.

## Background

I originally created this tool to simplify the process of finding and saving content for reposting. However, I realized that others might find it useful for various purposes, so I decided to make it publicly available.

## Features

- Asynchronous downloads for improved speed
- Progress bar to track download status
- Supports images (.jpg, .png), GIFs, and videos (.mp4)
- Error handling and logging
- Easy-to-use command-line interface

## Installation

1. Clone this repository:

   `git clone https://github.com/egdavid/reddit-media-downloader.git`

2. Navigate to the project directory:

   `cd reddit-media-downloader`

3. Install the required dependencies:

   `pip install -r requirements.txt`

## Usage

Run the script from the command line:

`python reddit_media_downloader.py`

When prompted, enter the Reddit username whose media you want to download.

The script will create a folder named after the username in the `downloads` directory and save all media files there.

## Disclaimer

This tool is intended for personal use only. Always respect copyright laws and Reddit's terms of service when using downloaded content. The author is not responsible for any misuse of this tool.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/egdavid/reddit-media-downloader/issues) if you want to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
