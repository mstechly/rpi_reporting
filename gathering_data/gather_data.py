import requests

def get_data(filename):
    # dummy data from http://apidev.accuweather.com/developers/samples
    api_url = 'http://apidev.accuweather.com/currentconditions/v1/14129.json?language=en&apikey=hoArfRosT1215'
    req = requests.get(api_url)
    response = req.text.encode('utf-8')
    f = open(filename, 'w')
    f.write(response)
    f.close()