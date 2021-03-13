import requests

USERID = '1041'
API_KEY = 'bbb3281e09670945b281'


def create_game(team_id_1: int, team_id_2: int):
	"""Create a game instance and return game ID."""
	url = "https://www.notexponential.com/aip2pgaming/api/index.php"
	payload='teamId1={}&teamId2={}&type=game&gameType=TTT'.format(team_id_1, team_id_2)
	headers = {
		'x-api-key': API_KEY,
		'userId': USERID,
		'Content-Type': 'application/x-www-form-urlencoded'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	return response.text['gameId']



