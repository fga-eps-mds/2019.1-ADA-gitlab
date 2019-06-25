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
        "status_code": {"type": "integer"}
    },
    "required": ["status_code"]
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

http_error_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Http error schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "status_code": {"type": "integer"}
    },
    "required": ["message", "status_code"]
}

message_error_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Wrong data",
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
}

pipeline_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Pipeline schema",
    "type": "object",
    "properties": {
        "job_id": {"type": "integer"},
        "branch": {"type": "string"},
        "commit": {"type": "string"},
        "job_name": {"type": "string"},
        "stage": {"type": "string"},
        "status": {"type": "string"},
        "web_url": {"type": "string"}
    },
    "required": ["web_url", "job_id", "branch", "commit", "stage",
                 "job_name", "status"]
}

build_messages_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Pipeline schema",
    "type": "object",
    "properties": {
        "jobs_message": {"type": "string"},
        "summary_message": {"type": "string"}
    },
    "required": ["jobs_message", "summary_message"]
}

views_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Pipeline schema",
    "type": "object",
    "properties": {
        "status": {"type": "string"}
        },
    "required": ["status"]
}
