import re
import requests
import time
from datetime import datetime
from database import db

BUCKET_NAME = "data-engineering-interns.macpaw.io"
TIME_TO_SLEEP = 300


def main():
    date = None
    with db.create_session() as session:
        while True:
            date = download_and_save_to_database(session, date)
            session.commit()
            time.sleep(TIME_TO_SLEEP)


def download_and_save_to_database(session, date):
    data = download_files_list()
    header = data.headers
    if header['Last-Modified'] == date:
        return date

    split_text = data.text.split("\n")
    saved_files = session.query(db.File)
    new_files = compare_data(split_text, saved_files)

    for file in new_files:
        db_file = db.File(file_name=file)
        session.add(db_file)
        for info in download_json_file(file):
            result = process_json_info(info)
            if result is not None:
                session.add(result)
        session.flush()
    return header['Last-Modified']


def process_json_info(info):
    if info["type"] == "song":
        return make_song(info)
    if info["type"] == "app":
        return make_app(info)
    if info["type"] == "movie":
        return make_movie(info)


def make_movie(info):
    movie_info = info["data"]
    original_title = movie_info["original_title"]
    movie_info["original_title_normalized"] = normalize(original_title)
    movie_info["release_date"] = datetime.strptime(movie_info["release_date"], '%Y-%m-%d')
    return db.Movie(**movie_info)


def make_app(info):
    app_info = info["data"]
    if app_info["rating"] == 5:
        app_info["is_awesome"] = True
    else:
        app_info["is_awesome"] = False
    return db.App(**info["data"])


def make_song(info):
    song_info = info["data"]
    song_info["ingestion_time"] = datetime.utcnow()
    return db.Song(**song_info)


def normalize(original_title):
    only_alnum = re.sub(r"[^\w\s]+", "", original_title, flags=re.U)  # delete all special symbols
    only_letters = re.sub(r"[0-9_]+", "", only_alnum).strip()  # delete all numbers and strip
    return re.sub(r"[\s]+", "_", only_letters.lower())  # replace all white spaces with "_"


def compare_data(split_text, saved_files):
    set_file = {file.file_name for file in saved_files}
    set_split_text = set(split_text)
    set_diff = set_split_text.difference(set_file)
    return set_diff


def download_files_list():
    url = f"https://{BUCKET_NAME}/files_list.data"
    data_list = requests.get(url, allow_redirects=True)
    return data_list


def download_json_file(file):
    url = f"https://{BUCKET_NAME}/{file}"
    json_file = requests.get(url, allow_redirects=True)
    return json_file.json()


if __name__ == '__main__':
    main()
