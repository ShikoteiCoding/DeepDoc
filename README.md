# DeepDoc
Docs writing should be easier. 
This project is for me to progress as a software developper and system design. The goal is to design the components to create a "Jira" like application. However, the goal is to implement document nesting: being able to create piece of information, use them in documents and keeping track of document versions by only updating the information instead of all the documents depending on this document.

For instance, when using "Company presentation document" we need to update each time the document is used because: Sales volume have changed / Dates have changed / Number of employees have changed etc etc.

So why not create those Pieces of information:
- Company Number Employees
- Company Yearly Revenue
- Company Sales Volume
- World Exposure

And use them in any document: \
"Company Presentation (for Investor)" \
  |__ "Number Employee" \
  |__ "Company Yearly Revenue" \
  |__ "Company Sales Volume"

"Company Presentation (for Customer)" \
  |__ "World Exposure" \
  |__ "Company Sales Volume"

# Installation
Everything is in the docker compose : database / api and backend logic. Soon to come : front.

## Docker commands
### Setup the containers
```
cd deep-doc
docker compose up
```

## Rebuild everything
```
cd deep-doc
docker compose up --build --force-recreate
```
### Delete
If need to debuild the docker because of schema change. Don't forget to delete both the container and the volume.

After a docker compose up you can :
```
docker compose down
```

## Python 
If you want to run outside docker, follow the following commands. Else, everything is managed by containers.
### Create a virtual env in a separate folder
```
cd ../
virtualenv venv
source venv/bin/activate
```

### Dependencies
```
pip install fastapi
pip install uvicorn[standard]
pip install psycopg2-binary
``` 

# Next Steps
- Features
    1. Duplicate a piece
    2. Historicy Tracking (more of a DB stuff ? - Who knows)
- Come up with simple front (demo only)
    1. Framework ?
    2. TS or JS
- DB
    1. Swhitch to Key-Value DB ? (thinking)
    2. Adding doc and piece title for search [half-done]
    3. Saving a doc with references should fill the rel table
    4. Connection pooling [half-done]
- Beautify
    1. Switch prints to proper logging system
    2. Switch to clean unit test, boring to deal with printer to test
    3. Create own exceptions for DB [half-done]
    4. Unnest if statements and raising errors 
    5. Add Optional edge cases on function / method returning None
    

## History
- Core functions (future back)
    1. Create a piece / doc [done]
    2. Modify a piece / doc [done]
    3. Simple parsing (for now) [done]
    4. Get all doc / pieces [done]
- DB
    1. Auto-increment on PK [done]
    2. Auto create date / update date ? [done]
    3. Switch DBLayerAccess error catching with context manager [done]
    4. Connection pooling (with auto management, nothing custom) [done]
    5. Use psycopg execute sql with parameters instead of using f-strings (not safe ?) [done]
- Beautify
    1. Refactor SQL DB execution [done]
    2. Active Record Pattern instead between records and object stores [done]
    3. Switch simple classes to dataclasses [done]
    4. Refactor Dataclasses to make them explicit (instead of dynamic instances from dict) [done]
- Dockerise
    1. Front docker compose [done]
    2. Back docker compose (one DB and one API) [done]


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