import time

import requests

import api_handler as api
from faker import Faker

fake = Faker(['ru-RU', 'en_US'])
Faker.seed(3)

PLAYLIST_AMOUNT = 20000

# api.add_new_user(1, "name")

# playlists = []
# for i in range(PLAYLIST_AMOUNT):
#     playlist = {'creator': 1, 'title': fake.word(), 'is_album': False}
#     playlists.append(playlist)
# start_time = time.time()
# response = requests.post(api.PLAYLIST_PATH, json=playlists)
# print("playlists added with time: ", time.time() - start_time)
# for i in range(1000):
#     file_id = fake.sha1(raw_output=False)
#     if i % 40 == 0:
#         print(i)
#     api.add_song(1, fake.random_int(min = 1, max=PLAYLIST_AMOUNT), fake.sentence(nb_words=4, variable_nb_words=False),
#                  file_id, None, None)
# print("songs added")
# print(str(requests.get(api.BASE_URL + '/song').json()))
start_time = time.time()
print(str(list(map(lambda s: s['title'], api.find_songs("слишком помимо")))), time.time() - start_time)
