# -*- coding: utf-8 -*-

import enum
import os
import requests
from flask import Flask, request
from pymessenger.bot import Bot
from bs4 import BeautifulSoup


app = Flask(__name__)

# this is a token to match FB fans page
# Light up
# ACCESS_TOKEN = "EAAEtsX9w5Q0BAHz42VnrkeSNajWpvJjc8ONCs4plPKlBzoafvDTxTEkVY1gGmTxiDcPKauUVHmACxSoyJ715dwhuvRV78QZCWKrQNnACFevghRzjU33xWYFuwZChpDTsVpnSZCtKmZBayMzOzXFdiWly9OZAJPgjgptYzBZAnivwZDZD"
# test bot
ACCESS_TOKEN = "EAACMTV0RjhoBADvhR8S2ZAw905cbZCQWZAFIAWYIl9JLw5Snqz6XSL2dqeSE6gP8kB3uW9iqJb7CAfiooqAdo5qXxZBIRWGvCL7rVXZBq3wkohaKX6HZBa3iuFq6Rpk55iiODQOpzX1VVupSWzqYXJfLkFfDn6QOkt3RIEAglLiAZDZD"
bot = Bot(ACCESS_TOKEN)


class InputType(enum.Enum):
    SONG = 0
    ALBUM = 1
    PLAYLIST = 2
    ARTIST = 3
    INQUERY = 4


SONG = 0
ALBUM = 1
PLAYLIST = 2
ARTIST = 3
INQUERY = 4

# response type
SINGLE = 0
LIST = 1

# error type
BAD_INPUT = -1
NO_RESULT = -2





# for verify
@app.route("/", methods=["GET"])
def handle_verification():
    if request.args["hub.verify_token"] == "test_for_verify":
        return request.args["hub.challenge"]
    else:
        return "Wrong Verify Token"


def get_access_token():
    return 0


# get web page
def get_web_page(url):
    response = requests.get(url)

    response.encoding = 'utf-8'
    if response.status_code != 200:
        print("Invalid url: ", response.url)
        return -1
    else:
        return response.text


def parse_web_html(doc):
    return BeautifulSoup(doc, "html.parser")


def get_web_title(soup):
    return soup.head.title


# reply request
def reply_text(user_id, message):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": message}
    }
    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)


def reply_greeting_message():
    data = {
        "setting_type": "greeting",
        "greeting": {
            "text": "請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\""
        }
    }


def reply_image_url(user_id, image_url):
    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url
                }
            }
        }
    }
    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(response.content)


def reply_generic_template(user_id, info):
    element = produce_elements(info)
    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "sharable": True,
                    "image_aspect_ratio": "square",
                    "elements": element
                }
            }
        }
    }
    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(response.content)


def reply_list_template(user_id, info):
    elements = produce_elements(info)
    buttons = produce_buttons(info)

    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "top_element_style": info["top_element_style"],
                    "elements": elements,
                    "buttons": buttons
                }
            }
        }
    }

    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(response.content)


def test(user_id):
    """generic template
    data = {
        "recipient":{
            "id":"USER_ID"
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "elements":[
                        {
                            "title":"Welcome to Peter\'s Hats",
                            "image_url":"https://petersfancybrownhats.com/company_image.png",
                            "subtitle":"We\'ve got the right hat for everyone.",
                            "default_action": {
                                "type": "web_url",
                                "url": "https://peterssendreceiveapp.ngrok.io/view?item=103",
                                "messenger_extensions": True,
                                "webview_height_ratio": "tall",
                                "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                            },
                            "buttons":[
                                {
                                    "type":"web_url",
                                    "url":"https://petersfancybrownhats.com",
                                    "title":"View Website"
                                },{
                                    "type":"postback",
                                    "title":"Start Chatting",
                                    "payload":"DEVELOPER_DEFINED_PAYLOAD"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    """
    # """open graph template
    data = {
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "open_graph",
                    "elements": [
                        {
                            "url": "https://open.spotify.com/track/7GhIk7Il098yCjg4BQjzvb",
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "https://www.kkbox.com/tw/tc/album/LkYUjLWHR0ueKJ0FvKA30091-index.html",
                                    "title": "View More"
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    # """
    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(response.content)


def set_sender_action(user_id, action):
    data = {
        "recipient": {
            "id": user_id
        },
        "sender_action": action
    }
    response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)


# print(response.content)

def handle_error_request(user_id, error_type):
    if error_type == BAD_INPUT:
        reply_text(user_id, "未設定之指令")
        reply_text(user_id, "請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"")
    elif error_type == NO_RESULT:
        reply_text(user_id, "抱歉～沒有尋找到任何資料")

    return 0


def search(inquiry, type, territory):
    payload = {"q": inquiry, "type": type, "territory": territory}
    headers = {"Authorization": "Bearer FDP48nJQc7DJD9MJtkhVqA=="}

    response = requests.get("https://api.kkbox.com/v1.1/search", params=payload, headers=headers)
    # print("content: ",response.json())
    # print("url: ",response.url)
    return response.json()


def result_num(json):
    num = json["summary"]["total"]
    if num >= 4:
        return 4
    elif num == 0:
        return 0
    return num


def artist_songs(id, territory):
    headers = {"Authorization": "Bearer FDP48nJQc7DJD9MJtkhVqA=="}
    return requests.get("https://api.kkbox.com/v1.1/artists/" + id + "/top-tracks?territory=" + territory + "&limit=5",
                        headers=headers).json()


def get_artist_info(json, index):
    name = json["artists"]["data"][index]["name"]
    url = json["artists"]["data"][index]["url"]
    image_url = json["artists"]["data"][index]["images"][1]["url"]
    return {"name": name, "url": url, "image_url": image_url}


def get_artist_name(mode, json):
    if mode == SONG:
        return json["tracks"]["data"][0]["album"]["artist"]["name"]
    elif mode == ALBUM:
        return json["albums"]["data"][0]["artist"]["name"]
    return "error"


def get_alblum_name(mode, json):
    if mode == SONG:
        return json["tracks"]["data"][0]["album"]["name"]
    elif mode == ALBUM:
        return json["albums"]["data"][0]["name"]
    return "error"


def matching_result(input, name):
    if name.find('(') >= 0:
        temp = name.lower().split("(")
        if input == temp[0][0:len(temp[0]) - 1]:
            return True
        else:
            return False
    else:
        if input == name.lower():
            return True
        else:
            return False


def produce_elements(info):
    elements = []
    if info["mode"] == InputType.SONG:
        webview_type = "compact"
    elif info["mode"] == InputType.ALBUM or info["mode"] == PLAYLIST or info["mode"] == ARTIST:
        webview_type = "tall"

    if info["response_type"] == SINGLE:
        elements.append({
            "title": info["name"],
            "image_url": info["widget_image_url"],
            "subtitle": info["subtitle"],
            "default_action": {
                "type": "web_url",
                "url": info["widget_song_url"],
                "webview_height_ratio": webview_type
            },
            "buttons": produce_buttons(info)
        })
        # print(elements)
        return elements
    else:
        if info["top_element_style"] == "large":
            elements = [{
                "title": info["songs_data"][0]["name"],
                "image_url": info["songs_data"][0]["image_url"],
                "default_action": {
                    "type": "web_url",
                    "url": info["songs_data"][0]["url"],
                    "webview_height_ratio": "full"
                }
            }]
            for i in range(1, info["num"] + 1):
                elements.append({
                    "title": info["songs_data"][i]["name"],
                    "subtitle": info["songs_data"][i]["subtitle"],
                    "image_url": info["songs_data"][i]["widget_image_url"],
                    "default_action": {
                        "type": "web_url",
                        "url": info["songs_data"][i]["widget_song_url"],
                        "webview_height_ratio": "compact"
                    }
                })
            return elements

        else:
            for i in range(0, info["num"]):
                elements.append({
                    "title": info["songs_data"][i]["name"],
                    "subtitle": info["songs_data"][i]["subtitle"],
                    "image_url": info["songs_data"][i]["widget_image_url"],
                    "default_action": {
                        "type": "web_url",
                        "url": info["songs_data"][i]["widget_song_url"],
                        "webview_height_ratio": webview_type
                    }
                })
            return elements


def produce_buttons(info):
    buttons = []
    if info["response_type"] == SINGLE:
        buttons = [{
            "type": "web_url",
            "url": info["web_url"],
            "title": "Web page"
        }]
        return buttons
    else:
        if info["top_element_style"] == "large":
            buttons = [{
                "type": "web_url",
                "url": info["songs_data"][0]["url"],
                "title": "Web page"
            }]
            return buttons
        else:
            buttons = [{
                "type": "web_url",
                "url": "https://www.kkbox.com/tw/tc/search.php?word=" + info["token"],
                "title": "More"
            }]
            return buttons


def return_mode(input):
    if input[1:] == "album" or input[1] == '#':
        return ALBUM
    elif input[1:] == "platlist" or input[1] == '$':
        return PLAYLIST
    else:
        return BAD_INPUT


def set_start_button():
    data = {
        "get_started": {
            "payload": "first_hand_shack"
        }
    }
    response = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + ACCESS_TOKEN,
                             json=data)


def modify_image_size(url, size):
    index = url.rfind("/")
    # print(index)
    if index > 0:
        temp = url[index + 1:]
        want_size = str(size) + "x" + str(size) + ".jpg"
        # print(size)
        if temp != want_size:
            # print(url[0:index+1] + "300x300.jpg")
            return url[0:index + 1] + want_size
        else:
            return url
    else:
        return url


def parse_request(message):
    song_index = message.find("聽")

    if message[0] == '/':
        return {"mode": InputType.SONG, "token": message[1:]}
    elif message[0] == '#':
        return {"mode": InputType.ALBUM, "token": message[1:]}
    elif message[0] == '$':
        return {"mode": InputType.PLAYLIST, "token": message[1:]}
    elif message[0] == '@':
        return {"mode": InputType.ARTIST, "token": message[1:]}
    """
    elif message[0] == '?':
        token = message.split(" ")
        token[0] = return_mode(token[0])
        return {"mode":INQUERY, "token":token}
    """

    if song_index < 0:
        return {"mode": BAD_INPUT}
    else:
        return {"mode": SONG, "token": message[song_index:]}


def get_info(msg, info_type):
    get = {
        InputType.SONG: _get_track,
        InputType.ALBUM: _get_album,
        InputType.PLAYLIST: _get_playlist,
        InputType.ARTIST: _get_artist,
    }

    try:
        info = get[info_type](msg)
    except KeyError:
        return ''
    return info

def _get_album(msg):
    pass

def _get_playlist(msg):
    pass

def _get_artist(msg):
    pass

def _get_track(msg):
    tracks = search(msg, 'track', 'TW')
    n = result_num(tracks)

    # If result is empty, fast fail
    if not n:
        return {'mode': NO_RESULT}

    # Check if we match the track
    for track in tracks['track']['data']:
        if msg in track:
            track_id = track['id']
            track_widget_url = get_widget_song_url(track_id)


            return {
                'mode': InputType.SONG,
                'response_type': SINGLE,
                'name': track['name'],
                'subtitle': '{album} {artist}'.format(album=track['album']['name'], artist=track['artist']['name']),
                'widget_song_url': track_widget_url,
                'widget_image_url': track['album']['images'][-1]['url'],
                'web_url': track['url']
            }

    # Return items when length > 0
    if tracks['track']['data']:
        pass

    return {'mode': NO_RESULT}



def find_info(token, mode):
    if mode == SONG:
        song_json = search(token, "track", "TW")
        num = result_num(song_json)
        if num > 0:
            if matching_result(token, song_json["tracks"]["data"][0]["name"]) or num == 1:
                song_id = get_song_id(song_json)
                print("id: ", song_id)
                widget_song_url = get_widget_song_url(song_id)

                return {
                    "mode": SONG,
                    "response_type": SINGLE,
                    "subtitle": get_alblum_name(mode, song_json) + "   " + get_artist_name(mode, song_json),
                    "widget_song_url": widget_song_url,
                    "name": get_widget_name(song_json, mode, 0),
                    "widget_image_url": modify_image_size(get_widget_image(song_json, mode, 0), 400),
                    "web_url": get_web_url(song_json, mode)
                }
            # return {"mode":SONG, "widget_song_url":widget_song_url, "web_title":web_title, "widget_image_url":widget_image_url}
            else:
                songs_data = []
                for i in range(0, num):
                    song_id = song_json["tracks"]["data"][i]["id"]
                    widget_song_url = get_widget_song_url(song_id)
                    songs_data.append({
                        "widget_song_url": widget_song_url,
                        "name": get_widget_name(song_json, mode, i),
                        "widget_image_url": get_widget_image(song_json, mode, i),
                        "subtitle": song_json["tracks"]["data"][i]["album"]["artist"]["name"]
                    })

                return {
                    "mode": SONG,
                    "num": num,
                    "token": token,
                    "response_type": LIST,
                    "top_element_style": "compact",
                    "songs_data": songs_data
                }
        elif num == 0:
            return {"mode": NO_RESULT}

    elif mode == ALBUM:
        album_json = search(token, "album", "TW")
        num = result_num(album_json)
        if num > 0:
            if matching_result(token, album_json["albums"]["data"][0]["name"]) or num == 1:
                album_id = get_album_id(album_json)
                print("id: ", album_id)
                widget_album_url = get_widget_album_url(album_id)

                return {
                    "mode": ALBUM,
                    "response_type": SINGLE,
                    "subtitle": get_artist_name(mode, album_json),
                    "widget_song_url": widget_album_url,
                    "name": get_widget_name(album_json, mode, 0),
                    "widget_image_url": modify_image_size(get_widget_image(album_json, mode, 0), 400),
                    "web_url": get_web_url(album_json, mode)
                }
            # return {"mode":ALBUM, "widget_song_url":widget_album_url, "web_title":web_title, "widget_image_url":widget_image_url}
            else:
                albums_data = []
                for i in range(0, num):
                    album_id = album_json["albums"]["data"][i]["id"]
                    widget_album_url = get_widget_album_url(album_id)
                    albums_data.append({
                        "widget_song_url": widget_album_url,
                        "name": get_widget_name(album_json, mode, i),
                        "widget_image_url": get_widget_image(album_json, mode, i),
                        "subtitle": album_json["albums"]["data"][i]["artist"]["name"]
                    })

                return {
                    "mode": ALBUM,
                    "num": num,
                    "token": token,
                    "response_type": LIST,
                    "top_element_style": "compact",
                    "songs_data": albums_data
                }
        else:
            return {"mode": NO_RESULT}
    elif mode == PLAYLIST:
        playlist_json = search(token, "playlist", "TW")
        num = result_num(playlist_json)
        if num > 0:
            if matching_result(token, playlist_json["playlists"]["data"][0]["title"]) or num == 1:
                playlist_id = get_playlist_id(playlist_json)
                print("id: ", playlist_id)
                widget_playlist_url = get_widget_playlist_url(playlist_id)

                return {
                    "mode": PLAYLIST,
                    "response_type": SINGLE,
                    "subtitle": playlist_json["playlists"]["data"][0]["description"],
                    "widget_song_url": widget_playlist_url,
                    "name": get_widget_name(playlist_json, mode, 0),
                    "widget_image_url": modify_image_size(get_widget_image(playlist_json, mode, 0), 400),
                    "web_url": get_web_url(playlist_json, mode)
                }
            # return {"mode":PLAYLIST, "widget_song_url":widget_playlist_url, "web_title":web_title, "widget_image_url":widget_image_url}
            else:
                playlists_data = []
                for i in range(0, num):
                    playlist_id = playlist_json["playlists"]["data"][i]["id"]
                    widget_playlist_url = get_widget_playlist_url(playlist_id)
                    playlists_data.append({
                        "widget_song_url": widget_playlist_url,
                        "name": get_widget_name(playlist_json, mode, i),
                        "widget_image_url": get_widget_image(playlist_json, mode, i),
                        "subtitle": playlist_json["playlists"]["data"][i]["description"]
                    })

                return {
                    "mode": PLAYLIST,
                    "num": num,
                    "token": token,
                    "response_type": LIST,
                    "top_element_style": "compact",
                    "songs_data": playlists_data
                }
        else:
            return {"mode": NO_RESULT}
    elif mode == ARTIST:
        artist_json = search(token, "artist", "TW")
        artist_num = result_num(artist_json)
        if artist_num > 0:
            if matching_result(token, artist_json["artists"]["data"][0]["name"]) or artist_num == 1:
                artist_id = get_artist_id(artist_json)
                print("id: ", artist_id)

                songs_data = [get_artist_info(artist_json, 0)]
                song_json = artist_songs(artist_id, "TW")
                # print(song_json)
                if "error" in song_json:
                    return {"mode": NO_RESULT}

                song_num = result_num(song_json)
                if song_num == 4:
                    song_num = 3

                for i in range(0, song_num):
                    song_id = song_json["data"][i]["id"]
                    widget_song_url = get_widget_song_url(song_id)
                    songs_data.append({
                        "widget_song_url": widget_song_url,
                        "name": get_widget_name(song_json["data"][i], mode, 0),
                        "subtitle": song_json["data"][i]["album"]["name"],
                        "widget_image_url": get_widget_image(song_json, mode, i)
                    })

                return {
                    "mode": ARTIST,
                    "num": song_num,
                    "response_type": LIST,
                    "top_element_style": "large",
                    "songs_data": songs_data
                }
            else:
                artists_data = []
                for i in range(0, artist_num):
                    artist_id = artist_json["artists"]["data"][i]["id"]
                    artist_info = get_artist_info(artist_json, i)
                    artists_data.append({
                        "widget_song_url": artist_info["url"],
                        "name": artist_info["name"],
                        "widget_image_url": artist_info["image_url"],
                        "subtitle": artist_info["name"]
                    })

                return {
                    "mode": ARTIST,
                    "num": artist_num,
                    "token": token,
                    "response_type": LIST,
                    "top_element_style": "compact",
                    "songs_data": artists_data
                }
        else:
            return {"mode": NO_RESULT}

    elif mode == INQUERY:
        return


def get_song_id(json):
    return json["tracks"]["data"][0]["id"]


def get_album_id(json):
    return json["albums"]["data"][0]["id"]


def get_playlist_id(json):
    return json["playlists"]["data"][0]["id"]


def get_artist_id(json):
    return json["artists"]["data"][0]["id"]


def get_web_url(json, mode):
    if mode == SONG:
        return json["tracks"]["data"][0]["url"]
    elif mode == ALBUM:
        return json["albums"]["data"][0]["url"]
    elif mode == PLAYLIST:
        return json["playlists"]["data"][0]["url"]


def get_widget_image(json, mode, index):
    if mode == SONG:
        return json["tracks"]["data"][index]["album"]["images"][0]["url"]
    elif mode == ALBUM:
        return json["albums"]["data"][index]["images"][0]["url"]
    elif mode == PLAYLIST:
        return json["playlists"]["data"][index]["images"][0]["url"]
    elif mode == ARTIST:
        return json["data"][index]["album"]["images"][0]["url"]


def get_widget_name(json, mode, index):
    if mode == SONG:
        return json["tracks"]["data"][index]["name"]
    elif mode == ALBUM:
        return json["albums"]["data"][index]["name"]
    elif mode == PLAYLIST:
        return json["playlists"]["data"][index]["title"]
    elif mode == ARTIST:
        return json["name"]


def get_widget_song_url(id):
    return "https://widget.kkbox.com/v1/?id=" + id + "&type=song"


def get_widget_album_url(id):
    return "https://widget.kkbox.com/v1/?id=" + id + "&type=album"


def get_widget_playlist_url(id):
    return "https://widget.kkbox.com/v1/?id=" + id + "&type=playlist"


def reply(user_id, info):
    set_sender_action(user_id, "mark_seen")
    set_sender_action(user_id, "typing_on")

    # test
    # test(user_id)
    # reply_text(user_id,'https://widget.kkbox.com/v1/?id=4qtXcj31wYJTRZbb23&type=album')

    # send text
    # reply_text(user_id,"https://www.google.com")

    # send image
    # reply_image_url(user_id,"http://pansci.asia/wp-content/uploads/2013/08/71a868311.jpg")
    # bot.send_image_url(user_id,"http://pansci.asia/wp-content/uploads/2013/08/71a868311.jpg")

    # send attachment
    # bot.send_attachment_url(user_id,"template","https://widget.kkbox.com/v1/?id=8sD5pE4dV0Zqmmler6&type=song")
    
    print(info)
    # if info["mode"] not in InputType:
    #     return 'ok'
    #     handle_error_request(user_id, info["mode"])
    # else:
    #     # print(info)
    if info["response_type"] == SINGLE:
        reply_generic_template(user_id, info)
    elif info["response_type"] == LIST:
        if info["top_element_style"] == "compact":
            if info["mode"] == SONG or info["mode"] == ARTIST:
                reply_text(user_id, "抱歉~沒有找到完全相同者\n請問是以下選項嗎？")
        reply_list_template(user_id, info)
    return 'ok'


@app.route("/", methods=["POST"])
def handle_incoming_message():
    data = request.json
    sender = data["entry"][0]["messaging"][0]["sender"]["id"]

    # handle first conversation
    if "postback" in data["entry"][0]["messaging"][0]:
        if data["entry"][0]["messaging"][0]["postback"]["payload"] == "first_hand_shack":
            reply_text(sender, "請輸入\"/歌曲名稱\"\n或輸入\"#專輯名稱\"\n或輸入\"$歌單名稱\"\n或輸入\"@歌手名稱\"")
            return "ok"

    # request with not pure text message
    if "attachments" in data["entry"][0]["messaging"][0]["message"]:
        response = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
        return "ok"

    text = data["entry"][0]["messaging"][0]["message"]["text"]
    print("message: ", text)

    request_token = parse_request(text)
    if request_token["mode"] not in InputType:
        handle_error_request(sender, request_token["mode"])
    else:
        info = get_info(request_token["token"], request_token["mode"])
        reply(sender, info)

    return "ok"


if __name__ == "__main__":
    set_start_button()
    app.run(debug=True)
