import os
import json
import requests
import urllib
import platform
from queue import Queue

class Donation:
    def __init__(self, id,createTime,amount,donatorName,message):
        self.id = id
        self.createTime = createTime
        self.amount = amount
        self.donator = donatorName
        self.message = message

    def __str__(self):
        return f"Donation(id={self.id}, createTime={self.createTime}, amount={self.amount}, donatorName={self.donator}, message={self.message})"

    def to_dict(self):
        return {
            "id": self.id,
            "createTime": self.createTime,
            "amount": self.amount,
            "donatorName": self.donator,
            "message": self.message
        }

class StreamlabsClient:
    def __init__(self):
        if platform.system() == 'Linux':
            self.token_path = "/home/ubuntu/gptconvo/gptconvo/streamlabsAccessToken.txt"
        elif platform.system() == 'Windows':
            home = os.path.expanduser("~")
            self.token_path = os.path.join(home, "Documents", "GPT", "streamlabsAccessToken.txt")
        else:
            raise Exception(f"Unsupported platform: {platform.system()}")

        self.access_token = self._load_access_token()
        if self.access_token is None:
            raise Exception("No Access Token supplied")

    def _load_access_token(self):
        if os.path.exists(self.token_path):
            with open(self.token_path, 'r') as f:
                return f.read()


    def getDonations(self, after=None):
        url = "https://streamlabs.com/api/v2.0/donations"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        params = {}
        if after is not None:
            params['after'] = after

        donations = Queue()
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Will raise an exception if the request failed
            data = response.json()

            # Sort donations data by donation_id
            sorted_donations_data = sorted(data['data'], key=lambda x: x['donation_id'])

            for donation_data in sorted_donations_data:
                donation = Donation(
                    donation_data['donation_id'],
                    donation_data['created_at'],
                    donation_data['amount'],
                    donation_data['name'],
                    donation_data['message']
                )
                donations.put(donation)

            return donations

        except:
            return donations

  
        


## STUFF FOR GETTING THE AUTH TOKEN IF WE NEED TO DO THAT AGAIN

data = {
    'grant_type': 'authorization_code',
    'client_id': 'a778bdf1-ab48-4d1c-9892-f822d60546b7',
    'client_secret': os.getenv("STREAMLABS_KEY"),
    'redirect_uri': 'http://localhost:9000/accesstoken',
    'code': 'def502004bcaa2e4a8e8afd6613935fff5eb3bd520685783fd241e68ff80c49b9793f515eaa87d0b776efccc3721a669719fb33c76125fcec0d41c947f2b0d01d2d21e94f215763e59582b93ef8f3c2c7426094ded92fa7deb140da7db382c987bbcb629a152b9311a9119bcd6ec0d8434cb1ce030cbbe07028fa62c93cd977ce9e839b679a882244f5100c0fa597715211ab15f9a32ade41d9253edddeae6a2814baf6d85133dc0cefdc70329b14b7b76aca27cd1da317d59f810532254f618907a7d2e9520dccc3ffe0aecf2864344aaa0a98d52d0b3278af92fbf28603dd39da6d509239dfa0004d3ce9caeb248afe2bf195d7a67ce60e6da0978981b46cd0d44a91b0c0ca8734b798372f5126e85e8b4fbd57eeaa9e25cd47e8f87d4f4e2a87673ef6441445d2ae626b46360b458043c8f7a6d8051c79ed3f06b95a6eb7ac2c9ff1905fe1af6b44b341b3433df0f926e2d7a949f059606357ae282aef36ea9c3c2165443dd7b0f58a9c11183e298b64d8c3377e54bc66c076cad7728d2695b1fc30e79ef8500a0bea6305ff6887fa461374685dcd9ae7a3c643b7c670e94a757c702662f34b1342df11d5e130f76b402ae458d3d3009507ce4f0b69df9fe9fabf0fe55e2552ef55553822857ad36ba8c51f5a809ec7e05988bbc352dd9b8cd7d8463470fa515cda05f34745eb1cfa9ce81330581bf09c046f09228e236b99b88b9741b81c0d05dab2c20ed8ae7f224fb1f00ca70625f586507d1591fc3e8073845467c9aba66d220137e800b38b60e2a2b17a8d1c82fb285e37b39d1eccbf1a40d04b756ad7f45f4e530c8f87d8417d9925c171af5ca680f'
}


base_url = 'https://streamlabs.com/api/v2.0/authorize'
params = {
    'response_type': 'code',
    'client_id': 'a778bdf1-ab48-4d1c-9892-f822d60546b7',
    'redirect_uri': 'http://localhost:9000/accesstoken',
    'scope': 'donations.create donations.read alerts.create legacy.token socket.token points.read points.write alerts.write credits.write profiles.write jar.write wheel.write mediashare.control',
}

url = base_url + '?' + urllib.parse.urlencode(params)







#response = requests.post('https://streamlabs.com/api/v2.0/token', data=data)
#token_info = response.json()
#access_token = token_info['access_token']
#print(access_token);