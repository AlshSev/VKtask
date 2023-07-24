import requests
import json

api_v = "5.131"
default_id = "51710748"

def get_auth_link(app_id=default_id, scope="friends"):
    link = (f"https://oauth.vk.com/authorize?client_id={app_id}&display=page"
            f"&redirect_uri=https://oauth.vk.com/blank.html&scope={scope}"
            f"&response_type=token&v={api_v}")
    return link

# Class used to create a specific method caller. 
# Initialized with method name, authorization token and parameter names. 
#
# Use call() to call (duh) the method. Input parameter values in the
# order corresponding to parameter names supplied during initialization.
class VKApiCaller:
    def __init__(self, method, token, *params):
        self.method = method;
        self.token = token;
        self.params = list(params)

    def call(self, *params_vals):
        link = self._build_link(*params_vals)
        response = requests.get(link)
        return response.text

    def _build_link(self, *params_vals):
        params_vals = list(params_vals)
        if len(params_vals) != len(self.params):
            raise Exception("Amount of values isn't equal to"
                            " amount of parameters")

        link = f"https://api.vk.com/method/{self.method}?"
        for param in zip(self.params, params_vals):
            link += "=".join(map(str, param)) + "&"
        link += f"access_token={self.token}&v={api_v}"
        return link

# Meant to represent a friend as described in the task, with an id thrown in
# for good measure. Sortable.
class VKUser:
    def __init__(self, user_id, fname, lname, country, city, bdate, sex):
        self.user_id = str(user_id)
        self.fname = str(fname)
        self.lname = str(lname)
        self.country = str(country)
        self.city = str(city)
        
        self.bdate = str(bdate)
        # Turns stuff like 7.2 into 07.02
        if self.bdate != "None":
            parts = self.bdate.split('.')
            new_parts = []
            for part in parts:
                if len(part) == 1:
                    new_parts.append('0' + part)
                else:
                    new_parts.append(part)
            self.bdate = '.'.join(new_parts)

        self.sex = str(sex)
        if self.sex != "None":
            match self.sex:
                case "0":
                    self.sex = "Not specified"
                case "1":
                    self.sex = "Female"
                case "2":
                    self.sex = "Male"
                case _:
                    self.sex = "Unknown"

    # Uses id to ensure uniqueness
    def __lt__(self, other):
        return (" ".join([self.fname, self.lname, self.user_id])
                < " ".join([other.fname, other.lname, other.user_id]))

def get_all_friends(user_id, token):
    friend_caller = VKApiCaller("friends.get", token, 
                                  "user_id", "offset", 
                                  "count", "fields")
    friends = []
    count = -1;

    while count != len(friends):
        # Uses 'count' = 1000. Can go up to 5000. Total friend limit is 10k.
        # So if you use 5000 you would need two calls at most (in theory).
        resp_text = friend_caller.call(user_id, len(friends), 1000, 
                                       "bdate,city,country,sex")
        resp_json = json.loads(resp_text)
        if "response" in resp_json:
            resp_json = resp_json['response']
        else:
            raise Exception("VK replied with the following error: "
                            f"{resp_text}")

        if "items" in resp_json:
            for friend in resp_json["items"]:
                fcountry = fcity = fbdate = None # These are optional
                if "country" in friend:
                    fcountry = friend["country"]["title"]
                if "city" in friend:
                    fcity = friend["city"]["title"]
                if "bdate" in friend:
                    fbdate = friend["bdate"]
                friends.append(VKUser(friend["id"], friend["first_name"], 
                                       friend["last_name"], fcountry,
                                       fcity, fbdate, friend["sex"]))

        count = int(resp_json["count"])

    friends.sort()
    return friends
