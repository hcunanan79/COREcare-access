# clients/geocoding.py
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

_geolocator = Nominatim(user_agent="bayarea-elite-homecare")
_geocode = RateLimiter(_geolocator.geocode, min_delay_seconds=1)

def geocode_address(address: str):
    """
    Returns (latitude, longitude) or (None, None)
    """
    if not address:
        return (None, None)

    try:
        location = _geocode(address)
        if not location:
            return (None, None)
        return (location.latitude, location.longitude)
    except Exception:
        return (None, None)
