# DeepDoc
Docs writing should be easier

# Docker commands
## Setup the db
```
cd deep-doc
docker compose up
```
## Delete
If need to debuild the docker because of schema change. Don't forget to delete both the container and the volume.

After a docker compose up you can :
```
docker rm db-deep-doc
docker volume rm deep-doc_deep-doc-data
```

# TODO
1. Setup the script (future back)
2. Dockerise the future back
3. Come up with simple front for demo
4. Dockerise simple front
5. Connect front with back

# Roadmap
## Comming Features
- Generate up to date doc (1 level deep)
- Add tag / version of doc

## Complex Features
- Recommand pieces
- Nested docs ?
- Custom script piece