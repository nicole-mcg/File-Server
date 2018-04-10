import requests, json

# url should be a string
# data_dict should be a dictionary of the data to send (should be json serializable)
# returns the recieved text if possible, otherwise returns None
def send_post_request(url, data_dict={}, cookie_dict = {}):
    r = requests.post(url, data=json.dumps(data_dict), cookies=cookie_dict)

    if r.status_code == 200:
        return r.text

    print(r.status_code)

    return None

# endpoint should be a string
def send_api_request(endpoint, session, data={}, port=8080):
    r = requests.post("http://127.0.0.1:{}/api/{}".format(port, endpoint), data=json.dumps(data), cookies={"session": session})

    if r.status_code == 200:
        return r.text

    return None