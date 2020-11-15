#!/bin/env bash

# Scan a Terraform JSON plan
#
# Detect any invalid names
#


# Case 1
# Logical resource names should not include any dashes. Only underscores should be used.
echo "Looking for invalid logical names"
cat $PLAN_J | jq '.planned_values.root_module.resources[] | select(.name | contains ("-")).address'



# Case 1
# Actual resource names should not include any underscores. Only dashes should be used.
echo "Looking for invalid resource names"
#cat $PLAN_J | jq '.planned_values.root_module.resources[].values | select (.name  | contains ("-")).name'

cat $PLAN_J | jq '.planned_values.root_module.resources[].values | select (.name != null) | select (.name | contains ("_")).name'

