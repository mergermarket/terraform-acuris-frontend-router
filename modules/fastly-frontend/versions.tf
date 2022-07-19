
terraform {
  required_version = ">= 0.13"
  required_providers {
    fastly = {
      version = "0.41.0"
      source = "fastly/fastly"
    }
    local = {
      source = "hashicorp/local"
    }
    template = {
      source = "hashicorp/template"
    }
  }
}