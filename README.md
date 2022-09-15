# UserProfile for EOSCF

The user profile component focuses on collecting in a centralised location all the information that we can gather
about the users of the portal. So far, its data sources are the Marketplace (MP) and the Recommender System (RS). In
the future we plan to utilize other internal sources like the AAI and external like OpenAIRE Graph.

https://wiki.eoscfuture.eu/display/EOSCF/User+Profile+Design+-+Version+1.0

## Initial set up

Prerequisites:
* docker
* docker-compose >= 1.24
* python >=3.9

**Step 1: Copy the dump files**
1. Copy the RS dump files to `storage/dumps/recommender/`

The final directory structure should look like:
```
storage/dumps/
  recommender/
    access_mode.bson
    access_mode.metadata.json
    recommendation.bson
    ...
```

**Step 2: Create the .env file**
```shell
USER_PROFILE_MONGO_HOST=localhost
USER_PROFILE_MONGO_PORT=27017
USER_PROFILE_MONGO_USERNAME="admin"
USER_PROFILE_MONGO_PASSWORD="admin"

USER_PROFILE_MONGO_DATABASE=user_profile
RS_MONGO_DB=rs_dump  # The database name in the RS dump used for initialization

DATABUS_HOST="eosc..."
DATABUS_PORT="1234..."
DATABUS_LOGIN="user"
DATABUS_PASSWORD="pass"

SENTRY_DSN="https://asdasd..."
CRONITOR_API_KEY=123123123...
```


**Step 3: User Profile DB initialization (~5min)**
1. Install the initial setup python requirements (`populate_profile_db/requirements.txt`)
2. Run `docker-compose -f docker-compose-init.yml up`
3. Run `python initialize_user_profile.py`


## Running

1. Run `docker-compose -f docker-compose-app.yml up`
2. Go to `http://localhost:4557/docs`, you should be able to see the docs
