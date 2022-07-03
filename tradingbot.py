import config, websocket, json

def on_open(ws):
    print("opened")
    auth_data = {
        "action":"auth",
        "key":config.API_KEY,
        "secret":config.SECRET_KEY
    }
    ws.send(json.dumps(auth_data))

    listen_message = {"action":"subscribe","trades":["SPY"],"quotes":["SPY"],"bars":["SPY"]}
    ws.send(json.dumps(listen_message))


def on_message(ws, message):
    print("recieved a message")
    print(message)







socket = config.STREAM_DATA_URL
ws = websocket.WbSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()


