from geopy.extra.rate_limiter import AsyncRateLimiter

async def get_location(geolocator, coordinates=False, name=False):
    if coordinates:
        reverse = AsyncRateLimiter(geolocator.reverse, min_delay_seconds=5, max_retries=3)
        res = await reverse(coordinates)
    if name:
        geocode = AsyncRateLimiter(geolocator.geocode, min_delay_seconds=5, max_retries=3)
        res = await geocode(name)
    if res is None:
        return False
    return res
