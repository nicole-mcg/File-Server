import requests, json

# Sends a post request to the specified URL
# url: the url string to send the request to
# data_dict: a dict containing any data to send. This will be turned into JSON
# cookie_dict: a dict containing any cookies to send with the request
def send_post_request(url, data_dict={}, cookie_dict = {}):

    # Send the request
    try:
        r = requests.post(url, data=json.dumps(data_dict), cookies=cookie_dict)
    except requests.exceptions.ConnectionError:
        # Couldn't connect
        return None

    # Check if the request was successful
    if r.status_code == 200:
        return r.text

    # Request wan't successful
    return None