import datetime
import pytz
#CDT: America/North_Dakota/Center
#London: Europe/London

def get_utc_timestamp() -> datetime.datetime:
    """_summary_
    Get a datetime object representing the current time in UTC
    
    Returns:
        datetime.datetime: current utc time
    """
    return datetime.datetime.now(datetime.timezone.utc)

def utc_to_local(utc_dt: datetime.datetime, local_tz: str ='Europe/London') -> datetime.datetime:
    """_summary_
    Convert a datetime object from UTC to a local timezone, which defaults to London if not specified.
    London Timzone: Europe/London
    Central Daylight Time: America/North_Dakota/Center
    
    Args:
        utc_dt (datetime.datetime): a utc datetime object
        local_tz (str, optional): Local timezone. Defaults to 'Europe/London'.

    Returns:
        datetime.datetime: the input datetime object in the local timezone
    """
    return utc_dt.astimezone(pytz.timezone(local_tz))

print(utc_to_local(get_utc_timestamp(), local_tz='America/North_Dakota/Center'))