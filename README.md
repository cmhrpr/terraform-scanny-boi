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


