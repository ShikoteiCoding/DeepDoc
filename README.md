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
    1. Create a piece / doc v0 [done]
    2. Modify a piece / doc
    3. Simple parsing (for now)
- Precise tech stack (dev not prod)
    1. Back
    2. Front
- Come up with simple front (demo only)
    1. Framework ?
    2. TS or JS
-  Dockerise
    1. Core functions are future back
    2. Front should be webpacked

## TODO
- Fix psycopg return type to fit in the models. Systematic mapping values to values ? [done]

# Roadmap
## Enhancements
- Use standarsized json-schema for models

## Comming Features
- Generate up to date doc (1 level deep)
- Add tag / version of doc

## Complex Features
- Recommand pieces
- Nested docs ?
- Custom script piece