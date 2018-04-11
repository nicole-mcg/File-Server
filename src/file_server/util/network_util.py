import requests, json

# url should be a string
# data_dict should be a dictionary of the data to send (should be json serializable)
# returns the recieved text if possible, otherwise returns None
def send_post_request(url, data_dict={}, cookie_dict = {}):
    try:
        r = requests.post(url, data=json.dumps(data_dict), cookies=cookie_dict)
    except requests.exceptions.ConnectionError:
        return None

    if r.status_code == 200:
        return r.text

    print(r.status_code)

    return None