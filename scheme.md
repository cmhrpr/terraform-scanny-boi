.planned_values = {}
root_module.resources = []

.address = MUST NOT CONTAIN "-"

.values = {}

name = Must not contain 

```console
$ cat plan.json | jq '.planned_values.root_module.resources[].address'
"aws_dynamodb_table.basic-dynamodb-table"
"aws_iam_role.iam_for_lambda"
"aws_lambda_function.test_lambda"



➜  tf git:(master) ✗ cat plan.json | jq 'select(.planned_values.root_module.resources[].address | contains ("asdsdasd"))'**

cat plan.json | jq '.planned_values.root_module.resources[] select (.address | contains("-"))'


➜  tf git:(master) ✗ cat plan.json | jq 'select(.planned_values.root_module.resources[].address | contains ("asdsdasd"))'**
```

How to find a logical name containing an invalid character

```
cat plan.json | jq '.planned_values.root_module.resources[] | select(.address | contains ("-")).address'
```

map(select(any(.Names[]; contains("data"))|not)|.Id)[]