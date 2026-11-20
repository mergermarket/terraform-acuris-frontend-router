
terraform {
  required_version = ">= 1.7.0" # `removed` blocks (fastly.tf) need 1.7+
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "> 5.47.0"
    }
  }
}
