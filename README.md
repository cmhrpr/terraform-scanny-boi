# Terraform naming schemes

[Wiki](https://app.nuclino.com/ttrx/personal/2020-11-15-Terraform-Naming-Schemes-4b6b6b83-070f-40e2-9444-b6873fc016a1)

## E2E

Requires:

* Terraform 0.12.29
* Python3.8

```console
cd tf
bash ../scripts/scan.sh
```


## Individual Jobs

### initialise 

Install Terraform 0.12.29 using Tfenv. This is configured in tf/.terraform-version

```console
cd tf
bash ../scripts/tf-init.sh
```

### Generate plan 

Generate a Terraform binary plan

```console
cd tf
bash ../scripts/tf-plan.sh
```


### Convert plan 

Generate a Terraform binary plan

```console
cd tf
bash ../scripts/tf-plan.sh
```


## Actual Plan

This will be distributed as a Python package via Pypi.

It will support reading a configuration file, and reading a Terraform plan in json format.

The rules in the configuration file will be applied to the Terraform plan, and the status of the rules will be reported back to the user in a report output file.

This is targeted at CICD pipelines, so should be added as a step after the creation of the Terraform plan. It will be useful to implement this to output a JUnit test report in XML format, as this can be easily read by Jenkins.

