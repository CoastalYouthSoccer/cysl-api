import requests
import logging

logger = logging.getLogger(__name__)


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
