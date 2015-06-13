import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data

def main():
    # results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    # pretty_print(results)

    # artist_id = results["artists"][1]["id"]
    # print "\nARTIST:"
    # pretty_print(results["artists"][1])

    # artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    # releases = artist_data["releases"]
    # print "\nONE RELEASE:"
    # pretty_print(releases[0], indent=2)
    # release_titles = [r["title"] for r in releases]

    # print "\nALL TITLES:"
    # for t in release_titles:
    #     print t

    # Q1: how many First Aid Kit bands?
    results = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    num = 0
    for i, artist in enumerate(results["artists"]):
    	if artist["name"].lower() == "first aid kit":
    		num += 1
    print num

    # Q2: begin_area name for Queen
    results = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    # pretty_print(results)
    for i, artist in enumerate(results["artists"]):
    	if artist["name"].lower() == "queen":
    		try:
    			print artist["begin-area"]["name"]
    		except:
    			None

    # Q3: Spanish alias for Beatles
    results = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    for i, artist in enumerate(results["artists"]):
    	try:
    		for j, alias in enumerate(artist["aliases"]):
    			if alias["locale"] == "es":
    				print alias["name"]
    	except:
    		None

    # Q4: Nirvana disambiguation
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    for i, artist in enumerate(results["artists"]):
    	if artist["name"].lower() == "nirvana":
    		try:
    			print artist["disambiguation"]
    		except:
    			None

    # Q5: When was 1D formed
    results = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    for i, artist in enumerate(results["artists"]):
    	if artist["name"].lower() == "one direction":
    		try:
    			print artist["life-span"]["begin"]
    		except:
    			None

if __name__ == '__main__':
    main()
