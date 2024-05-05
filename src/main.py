import requests
import base64
import subprocess
import os
import tqdm
from typing import List
from config import config

app_config: config.Config = config.from_file("config.json")
logs_buffer: List[str] = []

def main() -> None:
    headers: dict = {
        "Authorization": "Basic " + base64.b64encode(f"{app_config.username}:{app_config.api_key}".encode()).decode(),
        "User-Agent": f"E621 downloader with tags as EXIF data (in use by {app_config.username} on e621)"
    }

    download_all_favourites(headers, "output/")
    print("\n".join(logs_buffer))

def get_all_favourites(headers: dict) -> List[dict]:
    page: int = 1
    ret: List[dict] = []

    while True:
        posts: List[dict] = requests.get(f"https://e621.net/favorites.json?page={page}", headers=headers).json()["posts"]
        if len(posts) == 0:
            break
        
        ret += posts
        page += 1

    return ret

def download_all_favourites(headers: dict, output_dir: str = ""):
    for post in tqdm.tqdm(get_all_favourites(headers)):
        download_with_exif(post, output_dir)

def download_with_exif(post: dict, output_dir: str = ""):
    filename: str = output_dir + str(post["id"]) + "." + post["file"]["ext"]
    
    if os.path.exists(filename):
        logs_buffer.append(f"Warning: File {filename} already exists, not overwritten.")
        return

    if post["file"]["url"] is None:
        logs_buffer.append(f"Warning: The URL for {filename} was None, could not download.")
        return

    img_data: bytes = requests.get(post["file"]["url"]).content

    with open(filename, "wb") as fh:
        fh.write(img_data)

    if post["file"]["ext"] == "webm":
        logs_buffer.append(f"Warning: Skipped EXIF update on {filename} as WEBM is not yet supported")
        return

    all_tags: List[str] = ",".join([
        *post["tags"]["general"],
        *post["tags"]["artist"],
        *post["tags"]["copyright"],
        *post["tags"]["character"],
        *post["tags"]["species"],
        *post["tags"]["invalid"],
        *post["tags"]["meta"],
        *post["tags"]["lore"],
    ])

    try:
        with open(os.devnull, "wb") as devnull: 
            subprocess.check_call(["exiftool", f"-ImageDescription=\"{all_tags}\"", filename], stdout=devnull, stderr=devnull)
    except Exception as e: 
        logs_buffer.append(f"Warning: Could not apply exif data to {filename} - error {e}")
    
    subprocess.call(["rm", f"{filename}_original"])

if __name__ == "__main__": 
    main()
