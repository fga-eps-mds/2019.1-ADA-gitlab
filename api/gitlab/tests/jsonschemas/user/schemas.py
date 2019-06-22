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
    "type": "array",
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

user_valid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "repositories": {
            "type": "array",
        }
    },
    "required": ["repositories"]
}

user_invalid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "status_code": {"type": "integer"}
    },
    "required": ["message", "status_code"]
}

user_data_valid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User data schema",
    "type": "object",
    "properties": {
        "gitlab_username": {
            "type": "string",
        },
        "gitlab_user_id": {
            "type": "integer",
        }
    },
    "required": ["gitlab_username", "gitlab_user_id"]
}

project_id_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "project id schema",
    "type": "object",
    "properties": {
        "project_id": {
            "type": "integer"
        }
    },
    "required": ["project_id"]
}

user_id_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "user id schema",
    "type": "object",
    "properties": {
        "user_id": {
            "type": "integer"
        }
    },
    "required": ["user_id"]
}

get_user_project_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "get user project schema",
    "type": "object",
    "properties": {
        "repositories": {
            "type": "array"
        }
    },
    "required": ["repositories"]
}

save_user_domain_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "status": {"type": "string"}
    },
    "required": ["status"]
}

get_user_domain_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "get user domain schema",
    "type": "object",
    "properties": {
        "chat_id": {"type": "string"},
        "domain": {"type": "null"}
    },
    "required": ["chat_id", "domain"]
}

get_user_infos_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "get user infos domain schema",
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "repository": {"type": "string"}
    },
    "required": ["username", "repository"]
}

get_repo_name_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "get user infos domain schema",
    "type": "object",
    "properties": {
        "project_name": "string"
    },
    "required": ["project_name"]
}

get_repo_full_name_shcema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "get user infos domain schema",
    "type": "object",
    "properties": {
        "project_fullname": {"type": "string"}
    },
    "required": ["project_fullname"]

}
