# Personal Notes API (Flask)

A minimal Flask REST API that provides CRUD operations for personal notes.
- Runs on port 3001
- In-memory storage (easy to replace with a database later)
- OpenAPI/Swagger docs available at /docs

## Run
python run.py

Service will be available at: http://localhost:3001

OpenAPI/Swagger UI: http://localhost:3001/docs

## Endpoints

- GET /notes
- POST /notes
- GET /notes/<id>
- PUT /notes/<id>
- DELETE /notes/<id>

## Curl Examples

# List notes
curl -s http://localhost:3001/notes | jq .

# Create note
curl -s -X POST http://localhost:3001/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"First Note","content":"Hello world"}' | jq .

# Get note by id
curl -s http://localhost:3001/notes/1 | jq .

# Update note
curl -s -X PUT http://localhost:3001/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"content":"Updated content"}' | jq .

# Delete note
curl -s -X DELETE http://localhost:3001/notes/1 -i

## Notes on Storage

This API uses a simple in-memory dictionary:
- Keys: integer IDs
- Values: note objects with id, title, content

To replace with a database later:
- Swap out NOTES_STORE and NEXT_ID with a repository or service layer.
- Keep schemas and route handlers; only change the storage functions.
