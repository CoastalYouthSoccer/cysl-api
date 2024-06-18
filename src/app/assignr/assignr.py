from datetime import datetime
import requests
import logging
import re
from app.helpers.helpers import (format_date_yyyy_mm_dd, set_boolean_value)

logger = logging.getLogger(__name__)

START_TIME = '.startTime'
NOT_ASSIGNED = "Not Assigned"
SEARCH_START_DT = "search[start_date]"
SEARCH_END_DT = "search[end_date]"
ADMIN_REVIEW = ".adminReview"
ADMIN_NARRATIVE = ".adminNarrative"
CREW_CHANGES = ".crewChanges"
NARRATIVE = ".description"

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

def get_misconducts(payload):
    pattern = r'\.misconductGrid\.\d+\.name'
    found_cnt = get_match_count(payload, pattern)
    results = []
    for cnt in range(found_cnt):
        results.append({
            "name": payload[f'.misconductGrid.{cnt}.name'],
            "role": payload[f'.misconductGrid.{cnt}.role'],
            "team": payload[f'.misconductGrid.{cnt}.team'],
            "minute": payload[f'.misconductGrid.{cnt}.minute'],
            "offense": payload[f'.misconductGrid.{cnt}.offense'],
            "description": payload[f'.misconductGrid.{cnt}.description'],
            "pass_number": payload[f'.misconductGrid.{cnt}.passIdNumber'],
            "caution_send_off": payload[f'.misconductGrid.{cnt}.cautionSendOff']
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

def process_game_report(data):
    result = None
    if ADMIN_REVIEW not in data:
        if data[NARRATIVE]:
            data[ADMIN_REVIEW] = 'True'
        else:
            data[ADMIN_REVIEW] = None

    if ADMIN_NARRATIVE not in data:
        data[ADMIN_NARRATIVE] = None

    if CREW_CHANGES not in data:
        data[CREW_CHANGES] = None

    try:
        if NARRATIVE in data:
            narrative = data[NARRATIVE]
        else:
            narrative = None
        result = {
            "admin_review": set_boolean_value(data[ADMIN_REVIEW]),
            "misconduct": set_boolean_value(data['.misconductCheckbox']),
            'assignments_correct': set_boolean_value(data['.assignmentsCorrect']),
            'home_team_score': data['.homeTeamScore'],
            'away_team_score': data['.awayTeamScore'],
            'officials': get_referees(data),
            'author': data['.author_name'],
            'game_dt': data[START_TIME],
            'home_team': data['.homeTeam'],
            'away_team': data['.awayTeam'],
            'venue_subvenue': data['.venue'],
            'league': data['.league'],
            'age_group': data['.ageGroup'],
            'gender': data['.gender'],
            'misconducts': get_misconducts(data),
            'home_coach': 'Unknown',
            'away_coach': 'Unknown',
            'narrative': narrative,
            'ejections': set_boolean_value(data['.ejections']),
            'admin_narrative': data[ADMIN_NARRATIVE],
            'crewChanges': data[CREW_CHANGES]
        }

    except KeyError as ke:
        logging.error(f"Key: {ke}, missing from process_game_report")

    return result


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
        if not self.token:
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
                    venues.append({
                        'id': item['id'],
                        'name': item['name']
                    })
            except KeyError as ke:
                logging.error(f"Key: {ke}, missing from Venue response")

            page_nbr += 1
            if page_nbr > total_pages:
                more_rows = False

        return venues