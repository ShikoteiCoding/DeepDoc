# DeepDoc
Docs writing should be easier



# Installation
For now, the actions are not yet dockerized because it's still in a dev phase. So installing a virtualenv to manage the dependencies. The Database however is properly dockerize as it is pretty static.

## Docker commands
### Setup the db
```
cd deep-doc
docker compose up
```
### Delete
If need to debuild the docker because of schema change. Don't forget to delete both the container and the volume.

After a docker compose up you can :
```
docker rm db-deep-doc
docker volume rm deep-doc_deep-doc-data
```

## Python 
### Create a virtual env in a separate folder
```
cd ../
virtualenv venv
source venv/bin/activate
```

### Dependencies
```
pip install psycopg2-binary
``` 

# Next Steps
- Core functions (future back)
    1. Duplicate a piece
    2. Historicy Tracking (more of a DB stuff ? - Who knows)
- Precise tech stack (dev not prod)
    1. Back
    2. Front
- Come up with simple front (demo only)
    1. Framework ?
    2. TS or JS
-  Dockerise
    1. Core functions as future back
    2. Front should be webpacked
- DB
    1. Swhitch to Key-Value DB ? (thinking)
    2. Adding doc and piece title for search [half-done]
    3. Saving a doc with references should fill the rel table
- Beautify
    1. Switch prints to proper logging system
    2. Switch to clean unit test, boring to deal with printer to test
    3. Create own exceptions for DB [half-done]
    4. Unnest if statements and raising errors

## History
- Core functions (future back)
    1. Create a piece / doc [done]
    2. Modify a piece / doc [done]
    3. Simple parsing (for now) [done]
    4. Get all doc / pieces [done]
- DB
    1. Auto-increment on PK [done]
    2. Auto create date / update date ? [done]
- Beautify
    1. Refactor SQL DB execution [done]
    2. Active Record Pattern instead between records and object stores [done]
    3. Switch simple classes to dataclasses [done]


## TODO
- Fix psycopg return type to fit in the models. Systematic mapping values to values ? [done]
- Fix : DB Model is strict but Domain Model is not necessarely: for instance title can be None (should not)

# Roadmap
## Enhancements
- Use standarsized json-schema for models

## Comming Features
- Generate up to date doc (1 level deep) [done]
- Tree dependencies visualization
- Add tag / version of doc

## Complex Features
- Recommand pieces
- Nested docs ?
- Custom script piece