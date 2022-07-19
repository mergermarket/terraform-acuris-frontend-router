
terraform {
  required_version = ">= 0.13"
  required_providers {
    fastly = {
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