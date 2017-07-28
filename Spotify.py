#!/usr/bin/env python

import requests

LOGIN_URL = "https://accounts.spotify.com/api/login"

BON = "MHwwfDB8MHwxfDF8MXwx"

# Issue a get request to the website to get the csrf_token
def getCsrfToken():
	headers = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, sdch, br",
		"Accept-Language":"it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
		"Connection":"keep-alive",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	}

	result = requests.get("https://accounts.spotify.com/it-IT/login", headers=headers)		# Get request to the login page
	return result.cookies['csrf_token']	# Returning csfr_token needed for authentication

# Returns the dict with the data
def buildPayload(csrfToken,username,password):
	return {
  		'remember': 'true',
  		'username': username,
  		'password': password,
  		'csrf_token': csrfToken,
	}

# Returns the dict with the cookies
def buildCookies(csrfToken,username):
	return {
    	'__bon': BON,
    	'sp_t': '',
    	'sp_new': '1',
    	'spot': '',
    	'justRegistered': 'null',
    	'__tdev': 'QHMTxssj',
    	'__tvis': 'qx4MC7SP',
    	'csrf_token': csrfToken,
    	'_gat': '1',
    	'remember': username,
	}

# Performs the login and checks for account subscription
def login(username,password):
	token = getCsrfToken()

	payload = buildPayload(token,username,password)
	cookies = buildCookies(token,username)

	headers = {
	'Origin': 'https://accounts.spotify.com',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Accept': 'application/json, text/plain, */*',
	'Referer': 'https://accounts.spotify.com/it-IT/login',
	'Connection': 'keep-alive',
	}

	login = requests.post(LOGIN_URL, headers=headers, cookies=cookies, data=payload)	# Perform the login

	if 'displayName' in login.text:
		sub = requests.get("https://www.spotify.com/us/account/overview/", cookies=login.cookies)
		acc = sub.text

		sub = acc.split('<h3 class="product-name">')[1].split('</h3>')[0].replace('<span class="icon-checkmark-wrap"><svg><use xlink:href="#icon-checkmark"></use></svg></span>', '')

		if not "Free" in sub:
			exp = acc.split('<b class="recurring-date">')[1].split('</b>')[0]
		else:
			return [True,"Free"]
		return [True,sub+" until "+exp+",Country: "+acc.split('<p class="form-control-static" id="card-profile-country">')[1].split('</p>')[0]]
	else:
		return [False,"Not working"]
