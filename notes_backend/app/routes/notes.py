from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields, validate, EXCLUDE

# In-memory storage for notes; structured to be easily replaced by a DB layer later.
NOTES_STORE = {}
NEXT_ID = 1


class NoteBaseSchema(Schema):
    """Base schema for note validation."""
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=True, validate=validate.Length(min=1, max=200), description="Title of the note")
    content = fields.Str(required=True, validate=validate.Length(min=1), description="Content/body of the note")


class NoteCreateSchema(NoteBaseSchema):
    """Schema for creating a note."""
    pass


class NoteUpdateSchema(Schema):
    """Schema for updating a note; fields optional but must not be empty if provided."""
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=False, validate=validate.Length(min=1, max=200), description="Title of the note")
    content = fields.Str(required=False, validate=validate.Length(min=1), description="Content/body of the note")


class NoteSchema(NoteBaseSchema):
    """Schema for returning a full note with id."""
    id = fields.Int(required=True, description="Unique identifier of the note")


# Blueprint definition
blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="Endpoints for managing personal notes",
)


def _get_next_id() -> int:
    """Generate the next note ID."""
    global NEXT_ID
    nid = NEXT_ID
    NEXT_ID += 1
    return nid


def _get_note_or_404(note_id: int) -> dict:
    """Return a note by id or abort with 404."""
    note = NOTES_STORE.get(note_id)
    if not note:
        abort(404, message=f"Note with id={note_id} not found")
    return note


@blp.route("/")
class NotesCollection(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema(many=True), description="List all notes")
    def get(self):
        """Get a list of all notes.
        Returns a JSON array of note objects.
        """
        return list(NOTES_STORE.values())

    # PUBLIC_INTERFACE
    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteSchema, description="Created note")
    def post(self, json_data):
        """Create a new note.
        Body:
          - title: string (required)
          - content: string (required)
        Returns the created note with its id.
        """
        new_id = _get_next_id()
        note = {
            "id": new_id,
            "title": json_data["title"],
            "content": json_data["content"],
        }
        NOTES_STORE[new_id] = note
        return note


@blp.route("/<int:note_id>")
class NoteResource(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema, description="Requested note")
    def get(self, note_id: int):
        """Retrieve a specific note by ID."""
        return _get_note_or_404(note_id)

    # PUBLIC_INTERFACE
    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema, description="Updated note")
    def put(self, json_data, note_id: int):
        """Update an existing note by ID.
        Body may include any of:
          - title: string
          - content: string
        At least one field must be provided.
        """
        if not json_data:
            abort(400, message="No valid fields provided to update")
        note = _get_note_or_404(note_id)
        if "title" in json_data:
            note["title"] = json_data["title"]
        if "content" in json_data:
            note["content"] = json_data["content"]
        NOTES_STORE[note_id] = note
        return note

    # PUBLIC_INTERFACE
    @blp.response(204, description="Note deleted")
    def delete(self, note_id: int):
        """Delete a note by ID. Returns 204 No Content on success."""
        _get_note_or_404(note_id)
        del NOTES_STORE[note_id]
        return ""
