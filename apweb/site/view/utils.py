# -*- coding:utf-8 -*-

from copy import deepcopy
from pyramid.httpexceptions import HTTPNotFound


def serve_schema(schema, required=True):
    """Prepare a schema to be served by a view"""

    # Raise NotFound if schema is required and not available
    if schema is None and required:
            raise HTTPNotFound()

    # Don't modify the original schema
    schema = deepcopy(schema)

    # JSON schema defaults to not accepting null values, and UI can't distinguish them from false
    # So map None -> False/'', otherwise trying to validate input later will raise an error
    for prop in schema["properties"].values():
        # WARN Don't apply for enums as an empty string is sure to not be a valid option
        if prop.get("default") is None and "enum" not in prop:
            prop["default"] = False if prop["type"] == "boolean" else ""

    return schema
