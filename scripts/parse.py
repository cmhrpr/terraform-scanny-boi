import os
import sys

import json 


from util import TerraformError, validate_resource


# Import settings
plan_json_name = sys.argv[1]


# Set defaults
report = {}
data = None
errors = []


#
with open(plan_json_name) as json_file:
    data = json.load(json_file)



for planned_resource in data['planned_values']['root_module']['resources']:
    valid_tags = True 
    valid_name_logical = True
    valid_name_resource = True

    # Get values for this resource 
    resource_name_logical = planned_resource['name']
    for error in validate_resource(planned_resource):
        errors.append(error)


    # r_val = planned_resource['values']

    # print(f"Evaluating the resource {resource_name_logical}")

    
    # # Validate the Logical name
    # valid_name_logical = validate_logical_name(resource_name_logical)
    # if type(valid_name_logical) is TerraformError:
    #     errors.append(valid_name_logical)

    # # Validate name attribute if it is present
    # print("Validating resource name")

    # valid_name_resource = validate_resource_name(planned_resource)
    # if type(valid_name_resource) is TerraformError:
    #     errors.append(valid_name_resource)


    # valid_tags = validate_tag_set(planned_resource)
    # if type(valid_tags) is TerraformError:
    #     errors.append(valid_tags)
        

    # if validate_resource_name(planned_resource['values']['name']):
    #     print("hmmm")


    print("\n\n")


if errors != []:
    print(f"Found {len(errors)} errors.")
    for err_ in errors:
        print(err_)


