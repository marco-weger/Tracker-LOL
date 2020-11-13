from collections import deque
import requests

class Regions:
  RUSSIA = 'ru'
  KOREA = 'kr'
  BRAZIL = 'br1'
  OCEANIA = 'oc1'
  JAPAN = 'jp1'
  NORTH_AMERICA = 'na1'
  EUROPE_NORDIC_EAST = 'eun1'
  EUROPE_WEST = 'euw1'
  TURKEY = 'tr1'
  LATIN_AMERICA_NORTH = 'la1'
  LATIN_AMERICA_SOUTH = 'la2'

class RiotObserver:

  def __init__(self, key, default_region=(Regions.EUROPE_WEST)):
    self.key = key  #If you have a production key, use limits=(RateLimit(3000,10), RateLimit(180000,600),)
    self.default_region = default_region
    # Champions
    v = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]
    r = requests.get('http://ddragon.leagueoflegends.com/cdn/{v}/data/en_US/champion.json'.format(v=v))
    self.champions = r.json()['data']

  @staticmethod
  def sanitized_name(name):
    return name.replace(' ', '').lower()

  def base_request(self, region, request, value): # .. Yoohraiin7
    if region is None:
      region = self.default_region

    r = requests.get(
      'https://{region}.api.riotgames.com/lol/{request}{value}?api_key={key}'.format(
        region=region,
        request=request,
        value=value,
        key=self.key
      )
    )
    return r.json()

  def get_summoner_by_name(self, summoner_name, region=None):
    return self.base_request(region, 'summoner/v4/summoners/by-name/', self.sanitized_name(summoner_name))

  def get_current_game(self, summoner_id, region=None):
    return self.base_request(region, 'spectator/v4/active-games/by-summoner/', summoner_id)

  # TODO image???
  def get_champion_by_id(self, id):
    for key in self.champions:
      if int(id) == int(self.champions[key]['key']):
        return key
    return ''


# class LoLException(Exception):
#   def __init__(self, error, response):
#     self.error = error
#     self.headers = response.headers

#   def __str__(self):
#     return self.error

#   def __eq__(self, other):
#     if isinstance(other, "".__class__):
#       return self.error == other
#     elif isinstance(other, self.__class__):
#       return self.error == other.error and self.headers == other.headers
#     else:
#       return False

#   def __ne__(self, other):
#     return not self.__eq__(other)

#   def __hash__(self):
#     return super(LoLException).__hash__()


# error_400 = "Bad request"
# error_401 = "Unauthorized"
# error_403 = "Blacklisted key"
# error_404 = "Game data not found"
# error_405 = "Method not allowed"
# error_415 = "Unsupported media type"
# error_422 = "Player exists, but hasn't played since match history collection began"
# error_429 = "Too many requests"
# error_500 = "Internal server error"
# error_502 = "Bad gateway"
# error_503 = "Service unavailable"
# error_504 = 'Gateway timeout'

# def raise_status(response):
#   if response.status_code == 400:
#       raise LoLException(error_400, response)
#   elif response.status_code == 401:
#       raise LoLException(error_401, response)
#   elif response.status_code == 403:
#       raise LoLException(error_403, response)
#   elif response.status_code == 404:
#       raise LoLException(error_404, response)
#   elif response.status_code == 405:
#       raise LoLException(error_405, response)
#   elif response.status_code == 415:
#       raise LoLException(error_415, response)
#   elif response.status_code == 422:
#       raise LoLException(error_422, response)
#   elif response.status_code == 429:
#       raise LoLException(error_429, response)
#   elif response.status_code == 500:
#       raise LoLException(error_500, response)
#   elif response.status_code == 502:
#       raise LoLException(error_502, response)
#   elif response.status_code == 503:
#       raise LoLException(error_503, response)
#   elif response.status_code == 504:
#       raise LoLException(error_504, response)
#   else:
#       response.raise_for_status()