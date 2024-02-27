# %%
import instagrapi
import instagrapi.types as types
from instagrapi import Client
from pydantic_core import Url
import json
from typing import *
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv

# %%
load_dotenv()
ecl = Client()
ecl.login(username=os.environ["user"], password=os.environ["pass"])
efollowers = ecl.user_followers(ecl.user_id)

#%%
def transform_follower(client: Client, follower: int) -> Tuple[int, types.User]:
    return (follower, client.user_info(str(follower)))

def transform_followers(client: Client, followers: Dict[int, types.UserShort]) -> Dict[int, types.User]:
    res = {}
    with ThreadPoolExecutor(max_workers=256) as pool:
        for fid, follower in pool.map(lambda f: transform_follower(client, f), followers):
            print(fid, follower)
            res[fid] = follower

    return res

def clean_followers(followers: Dict[int, types.User]) -> Dict[int, dict]:
    res = {}
    all_fields = {
        "pk", "username", "full_name", "is_private", "profile_pic_url", "profile_pic_url_hd", "is_verified",
        "media_count", "follower_count", "following_count", "biography", "external_url", "account_type",
        "is_business", "public_email", "contact_phone_number", "public_phone_country_code", "public_phone_number",
        "business_contact_method", "business_category_name", "category_name", "category", "address_street",
        "city_id", "city_name", "latitude", "longitude", "zip", "instagram_location_id", "interop_messaging_user_fbid"
    }

    interesting_fields = ["username", "full_name", "is_verified",
                          "media_count", "follower_count", "following_count",
                          "biography", "external_url", "account_type", "public_email", "category"]
    for id, info in followers.items():
        res[id] = {}
        for field in interesting_fields:
            assert hasattr(info, field)
            res[id][field] = str(getattr(info, field))

    return res

def serialize(obj):
    if isinstance(obj, Url):
        return str(obj)
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()
    return obj

# %%
edict_followers = transform_followers(ecl, efollowers)

# %%
print(type(edict_followers))
cleaned = clean_followers(edict_followers)
with open("efollowers.json", "w") as f:
    json.dump(cleaned, f)


# %%
first_user = ecl.user_info('4354975239')

#%%
lana = ecl.user_info_by_username('lana_photoset')
#%%
oli = ecl.user_info_by_username('matildathemann')
oli.account_type
#%%
print(json.dumps(first_user.model_dump(), indent=4, default=serialize, ensure_ascii=False))
with open("oli_info.json", "w") as f:
    json.dump(oli.model_dump(), f, indent=4, default=serialize, ensure_ascii=False)