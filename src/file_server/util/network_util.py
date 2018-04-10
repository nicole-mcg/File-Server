import requests, json

# url should be a string
# data_dict should be a dictionary of the data to send (should be json serializable)
# returns the recieved text if possible, otherwise returns None
def send_post_request(url, data_dict):
    r = requests.post(url, data=json.dumps(data_dict))
    if r.status_code == 200:
        return r.text
    return None