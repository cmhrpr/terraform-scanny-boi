import re 

valid_errors = {
    "tags_not_found": "The tag attribute was not present",
    "tags_set_none": "The tag attribute was found, but set to None",
    "tags_missing": "A required tag is missing. Please see error.info",
    "invalid_name_logical": "The logical name is invalid",
    "name_resource_invalid": "The resource name is invalid",
    "name_resource_set_none": "The name attribute was found, but set to None",
    "name_resource_not_found": "The name attribute was not present",
}



attribute_names = {
    "aws_lambda_function": {
        "name": "function_name"
    }
}


class TerraformError:
    """
        Represents an error found while validating a Terraform plan.
    """
    def __init__(self, logical_name, error, info=None):
        if error not in valid_errors:
            exit(f"INVALID ERROR {error} MUST BE IN {valid_errors.keys()}")

        self.logical_name = logical_name 
        self.error = error
        self.info = info

    def __str__(self):
        return f"{self.logical_name}: {self.error} - {self.info}"



def validate_logical_name(logical_name):
    """
        Ensure the logical name of a Terraform resource is valid
    """ 

    p = re.compile('^[a-zA-Z0-9_]+$')
    result = p.match(logical_name)
    
    if result is None:
        return TerraformError(logical_name, "invalid_name_logical", "invalid character found. logical name must match '^[a-zA-Z0-9_]+$'")

    return 1


def validate_resource_name(resource):
    """
        Ensure the logical name of a Terraform resource is valid

        :param resource_name: The name that has been given to a Terraform resource 
    """ 

    logical_name = resource['name']

    resource_type = resource['type']

    name_attribute = 'name'

    if resource_type in attribute_names:
        name_attribute = attribute_names[resource_type]['name']

    if name_attribute not in resource['values']:
        return TerraformError(logical_name, "name_resource_not_found")

    resource_name = resource['values'][name_attribute]

    if resource_name is None:
        return TerraformError(logical_name, "name_resource_set_none")

    p = re.compile('^[a-zA-Z0-9-]+$')
    result = p.match(resource_name)
    
    if result is None:
        return TerraformError(logical_name, "name_resource_set_none", resource_name)
    return 1

def validate_tag_set(resource):
    """
        Validate a set of Terraform tags

        :param tags: dict of tag values
    """

    logical_name = resource['name']

    if 'tags' not in resource['values']:
        return TerraformError(logical_name, "tags_not_found")

    tags = resource['values']['tags']
    if tags is None:
        return TerraformError(logical_name, "tags_set_none")

    tags_required = ["Name", "Environment", "Project"]

    tags_found = []
    tags_missing = []

    valid = True 

    for tag_key in tags:
        tags_found.append(tag_key)

    tags_missing = set(tags_required) - set(tags_found)
    
    if len(tags_missing) > 0:
        return TerraformError(logical_name, "tags_missing", tags_missing)


    return valid 
