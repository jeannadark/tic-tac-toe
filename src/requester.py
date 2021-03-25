import requests
import http.client
import ast

USERID = "1041"
API_KEY = "bbb3281e09670945b281"
TEAM_ID = "1244"
url = "https://www.notexponential.com/aip2pgaming/api/index.php"


def create_game(opponent_team: int):
    """Create a game instance and return game ID."""
    payload = (
        "teamId1="
        + TEAM_ID
        + "&teamId2="
        + str(opponent_team)
        + "&type=game&gameType=TTT"
    )
    headers = {
        "x-api-key": API_KEY,
        "userId": USERID,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    conn = http.client.HTTPSConnection('www.notexponential.com')

    conn.request("POST", '/aip2pgaming/api/index.php', payload, headers)
    response = conn.getresponse()
    data = response.read()

    return ast.literal_eval(data.decode('utf-8'))["gameId"]


def make_a_move(game_id: int, move: tuple):
    """Make a move."""
    x, y = move
    payload = (
        "teamId="
        + TEAM_ID
        + "&move="
        + str(x)
        + "%2C"
        + str(y)
        + "%20&type=move&gameId="
        + str(game_id)
    )
    headers = {
        "x-api-key": API_KEY,
        "userId": USERID,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    conn = http.client.HTTPSConnection('www.notexponential.com')
    conn.request("POST", '/aip2pgaming/api/index.php', payload, headers)
    response = conn.getresponse()
    data = response.read()
    # print(ast.literal_eval(data.decode('utf-8')))


def get_move_list(game_id: int, count: int = 2):
    """Get list of recent moves made for the game instance. Defaults to 2 recent moves."""
    get_moves_url = (
        "/aip2pgaming/api/index.php?type=moves&gameId="
        + str(game_id)
        + "&count="
        + str(count)
    )
    payload = {}
    headers = {
        "x-api-key": API_KEY,
        "userId": USERID,
    }

    conn = http.client.HTTPSConnection('www.notexponential.com')
    conn.request("GET", get_moves_url, payload, headers)
    response = conn.getresponse()
    data = response.read()
    # print(data)
    # print(ast.literal_eval(data.decode('utf-8')))

    return ast.literal_eval(data.decode('utf-8'))


def get_board_map(game_id: int):
    """Print board map."""
    board_map_url = (
        "/aip2pgaming/api/index.php?type=boardMap&gameId="
        + str(game_id)
    )
    payload = {}
    headers = {"x-api-key": API_KEY, "userId": USERID}

    conn = http.client.HTTPSConnection('www.notexponential.com')
    conn.request("GET", board_map_url, payload, headers)
    response = conn.getresponse()
    data = response.read()

    # print(data)