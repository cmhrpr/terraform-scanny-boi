import os

import json 
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

class TerraformError:
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
        return TerraformError(logical_name, "invalid_name_logical")

    return 1


def validate_resource_name(resource):
    """
        Ensure the logical name of a Terraform resource is valid

        :param resource_name: The name that has been given to a Terraform resource 
    """ 

    logical_name = resource['name']

    if 'name' not in resource['values']:
        return TerraformError(logical_name, "name_resource_not_found")

    resource_name = resource['values']['name']

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

# Import settings
plan_json_name = os.environ["PLAN_J"]


# Set defaults
report = {}
data = None
errors = []






with open(plan_json_name) as json_file:
    data = json.load(json_file)



for planned_resource in data['planned_values']['root_module']['resources']:
    valid_tags = True 
    valid_name_logical = True
    valid_name_resource = True

    # Get values for this resource 
    resource_name_logical = planned_resource['name']


    r_val = planned_resource['values']

    print(f"Evaluating the resource {resource_name_logical}")

    
    # Validate the Logical name
    valid_name_logical = validate_logical_name(resource_name_logical)
    if type(valid_name_logical) is TerraformError:
        errors.append(valid_name_logical)

    # Validate name attribute if it is present
    print("Validating resource name")

    valid_name_resource = validate_resource_name(planned_resource)
    if type(valid_name_resource) is TerraformError:
        errors.append(valid_name_resource)


    valid_tags = validate_tag_set(planned_resource)
    if type(valid_tags) is TerraformError:
        errors.append(valid_tags)
        

    # if validate_resource_name(planned_resource['values']['name']):
    #     print("hmmm")


    print("\n\n")


if errors != []:
    print(f"Found {len(errors)} errors.")
    for err_ in errors:
        print(err_)


