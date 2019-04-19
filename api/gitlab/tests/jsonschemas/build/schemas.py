ping_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "status": {"type": "string"}
    },
    "required": ["message", "status"]
}

valid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "branch": {"type": "string"},
        "commit": {"type": "string"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "name1": {"type": "string"},
        "stage": {"type": "string"},
        "status": {"type": "string"},
        "status1": {"type": "string"},
        "web_url": {"type": "string"}
    },
    "required": ["branch", "commit", "id", "name", "name1",
                 "stage", "status", "status1", "web_url"]
}

unauthorized_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "status_code": {"type": "integer"}
    },
    "required": ["status_code"]
}

invalid_project_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "status_code": {"type": "integer"}
    },
    "required": ["status_code"]
}

build_valid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "branch": {"type": "string"},
        "commit": {"type": "string"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "name1": {"type": "string"},
        "stage": {"type": "string"},
        "status": {"type": "string"},
        "status1": {"type": "string"},
        "web_url": {"type": "string"}
    },
    "required": ["branch", "commit", "id", "name", "name1",
                 "stage", "status", "status1", "web_url"]
}

build_invalid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "status_code": {"type": "integer"}
    },
    "required": ["message", "status_code"]
}
