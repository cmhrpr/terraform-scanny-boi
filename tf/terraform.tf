terraform {
  backend "s3" {
    bucket = "tfstate-cmhrpr"
    key    = "scanner_boi"
    region = "eu-west-1"
  }
}
