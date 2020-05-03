from copy import deepcopy
from typing import Any, Dict

from .utils import traverse_schema


def to_json_schema(schema: Dict[str, Any], nullable_name: str) -> Dict[str, Any]:
    """Convert Open API parameters to JSON Schema.

    NOTE. This function is applied to all keywords (including nested) during schema resolving, thus it is not recursive.
    See a recursive version below.
    """
    schema = deepcopy(schema)
    if schema.get(nullable_name) is True:
        del schema[nullable_name]
        if schema.get("in"):
            initial_type = {"type": schema["type"]}
            if schema.get("enum"):
                initial_type["enum"] = schema.pop("enum")
            schema["anyOf"] = [initial_type, {"type": "null"}]
            del schema["type"]
        else:
            schema = {"anyOf": [schema, {"type": "null"}]}
    if schema.get("type") == "file":
        schema["type"] = "string"
        schema["format"] = "binary"
    return schema


def to_json_schema_recursive(schema: Dict[str, Any], nullable_name: str) -> Dict[str, Any]:
    """Apply ``to_json_schema`` recursively.

    This version is needed for cases where the input schema was not resolved and ``to_json_schema`` wasn't applied
    recursively.
    """
    return traverse_schema(schema, to_json_schema, nullable_name)
