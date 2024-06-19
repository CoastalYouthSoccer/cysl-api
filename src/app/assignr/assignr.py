import requests
import logging
import re

logger = logging.getLogger(__name__)

START_TIME = '.startTime'
NOT_ASSIGNED = "Not Assigned"
SEARCH_START_DT = "search[start_date]"
SEARCH_END_DT = "search[end_date]"

def get_match_count(data, match):
    pattern = re.compile(match)

    return sum(1 for key in data.keys() if pattern.match(key))
 
def get_referees(payload):
    pattern = r'\.officials\.\d+\.position'
    found_cnt = get_match_count(payload, pattern)
    results = []
    for cnt in range(found_cnt):
        results.append({
            "name": payload[f'.officials.{cnt}.name'],
            "position": payload[f'.officials.{cnt}.position']
        })

# Make sure three referees are in the dictionary. Assumes missing positions are ARs
    for cnt in range(found_cnt, 3):
        results.append({
            "name": NOT_ASSIGNED,
            "position": "Asst. Referee"
        })
    return results

def get_game_information(payload):
    return {
        'id': payload["id"],
        'date': payload["localized_date"],
        'time': payload["localized_time"],
        'start_time': payload["start_time"],
        'home_team': payload["home_team"],
        'away_team': payload["away_team"],
        'age_group': payload["age_group"],
        'league': payload["league"],
        'venue': payload["venue"],
        'gender': payload["gender"],
        'sub_venue': payload["subvenue"],
        'game_type': payload["game_type"],
    }

def get_referees_by_assignments(payload):
    referees = []
    first_name = None
    last_name = None
    for official in payload:
        if '_embedded' in official and \
            'official' in official['_embedded']:
            first_name = official['_embedded']['official']['first_name']
            last_name = official['_embedded']['official']['last_name']
        referees.append({
            'accepted': official['accepted'],
            'position': official['position'],
            'first_name': first_name,
            'last_name': last_name
        })
    return referees


class Assignr:
    def __init__(self, client_id, client_secret, client_scope,
                 base_url, auth_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_scope = client_scope
        self.base_url = base_url
        self.auth_url = auth_url
        self.site_id = None
        self.token = None

    def authenticate(self) -> None:
        form_data = {
            'client_secret': self.client_secret,
            'client_id': self.client_id,
            'scope': self.client_scope,
            'grant_type': 'client_credentials'
        }

        authenticate = requests.post(self.auth_url, data=form_data)

        try:
            self.token = authenticate.json()['access_token']
        except (KeyError, TypeError):
            logging.error('Token not found')
            self.token = None

    def get_site_id(self) -> None:
        rc, response = self.get_requests('/sites')
        try:
            if rc == 200:
                self.site_id = response['_embedded']['sites'][0]['id']
            else:
                logging.error(f"Response code {rc} returned for get_site_id")     
        except (KeyError, TypeError):
            logging.error('Site id not found')

    def get_requests(self, end_point, params=None):
        self.authenticate()

        headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self.token}'
        }

        # Logic manages pagination url
        if self.base_url in end_point:
            response = requests.get(end_point, headers=headers, params=params)
        else:
            response = requests.get(f"{self.base_url}{end_point}", headers=headers, params=params)
        return response.status_code, response.json()

    def get_venues(self):
        more_rows = True
        venues = []
        page_nbr = 1

        if self.site_id is None:
            self.get_site_id()

        while more_rows:
            params = {
                'page': page_nbr
            }
            status_code, response = self.get_requests(f'sites/{self.site_id}/venues',
                                                      params=params)
            if status_code != 200:
                logging.error(f'Failed to get venues: {status_code}')
                more_rows = False
                return venues

            try:
                total_pages = response['page']['pages']
                for item in response['_embedded']['venues']:
                    city = item['city'] if 'city' in item else None
                    venues.append({
                        'id': item['id'],
                        'name': item['name'],
                        'city': city
                    })
            except KeyError as ke:
                logging.error(f"Key: {ke}, missing from Venue response")

            page_nbr += 1
            if page_nbr > total_pages:
                more_rows = False

        return venues

    def get_games(self, start_dt, end_dt, league=None, venue=None):
        more_rows = True
        results = []
        page_nbr = 1

        params = {
            SEARCH_START_DT: start_dt,
            SEARCH_END_DT: end_dt
        }

        if self.site_id is None:
            self.get_site_id()

        while more_rows:
            params['page'] = page_nbr
            status_code, response = self.get_requests(f'sites/{self.site_id}/games',
                                                      params=params)
            if status_code != 200:
                logging.error(f'Failed to get games: {status_code}')
                more_rows = False
                return results

            try:
                total_pages = response['page']['pages']
                for item in response['_embedded']['games']:
                    sub_items = item['_embedded']
                    if item['league'] == league or \
                        sub_items['venue']['name'] == venue or \
                        league is None or venue is None:
                        assignor = f'{sub_items["assignor"]["first_name"]}' \
                        f' {sub_items["assignor"]["last_name"]}' \
                            if 'assignor' in sub_items else None
                        referees = get_referees_by_assignments(sub_items['assignments'])
                        sub_venue = item['subvenue'] if 'subvenue' in item else None
                        game_type = item['game_type'] if 'game_type' in item else None
                        results.append({
                            'officials': referees,
                            'game_date': item["localized_date"],
                            'game_time': item["localized_time"],
                            'home_team': item["home_team"],
                            'away_team': item["away_team"],
                            'venue': sub_items["venue"]["name"],
                            'sub_venue': sub_venue,
                            'game_type': game_type,
                            'age_group': item["age_group"],
                            'gender': item["gender"],
                            'assignor': assignor
                    })
            except KeyError as ke:
                logging.error(f"Key: {ke}, missing from Game response")

            page_nbr += 1
            if page_nbr > total_pages:
                more_rows = False

        return results
