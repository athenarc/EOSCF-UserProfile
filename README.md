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
2. Copy the marketplace dump file (`.sql`) to `storage/dumps/marketplace/`

The final directory structure should look like:
```
storage/dumps/
  marketplace/
    mp_dump_name.sql
  recommender/
    access_mode.bson
    access_mode.metadata.json
    recommendation.bson
    ...
```

**Step 2: Set up the credentials**
1. Change the default values for usernames and passwords in `credentials.yml`


**Step 3: User Profile DB initialization (~4min)**
1. Install the initial setup python requirements (`populate_profile_db/requirements.txt`)
2. Run `populate_profile_db/main.py`


## Running

1. Run `docker-compose -f docker-compose-app.yml up`
2. Go to `http://localhost:4557/docs`, you should be able to see the docs
