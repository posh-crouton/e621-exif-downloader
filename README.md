# e621 downloader with EXIF data

## Description

A tool to download your favourite [e621](https://e621.net/) posts, including their e621 tags in the downloaded images' EXIF data. 

## Installation

If you're running linux: 
1. Clone the repository
2. Add execution permission to `src/start.sh`
3. Run `src/start.sh`

You may be prompted for some apt installations. These are to ensure that the virtual environment can be made and that the program can write exif data. 

## Limitations

Due to limitations with libimage-exiftool-perl (version 12.40+dfsg-1), this program cannot add EXIF data to `.webm` files. While they will still be downloaded, their EXIF data will not be stored on disk. 