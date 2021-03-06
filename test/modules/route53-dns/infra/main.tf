terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  version                     = ">= 2.15"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_get_ec2_platforms      = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
  max_retries                 = 1
  access_key                  = "a"
  secret_key                  = "a"
  region                      = "eu-west-1"
}

module "route53_dns" {
  source = "../../../../modules/route53-dns"

  domain  = "test.com"
  name    = "test"
  env     = "dev"
  target  = "target.test.com"
  zone_id = "TESTZONEID"
}

module "route53_dns_alias" {
  source = "../../../../modules/route53-dns"

  domain      = "test.com"
  name        = "test"
  env         = "dev"
  target      = "target.test.com"
  alb_zone_id = "ABCDE012345"
  alias       = "1"
  zone_id     = "TESTZONEID"
}
