variable "domain" {
  description = "The domain to use as a base"
}

variable "name" {
  description = "The name of the component to build a domain for"
}

variable "env" {
  description = "The environment this component is running in"
}

variable "target" {
  description = "Where the DNS should send traffic"
}

variable "ttl" {
  description = "The TTL for the dns record"
  default     = 60
}

variable "alias" {
  description = "Create an alias rather than a CNAME"
  default     = false
}

variable "alb_zone_id" {
  description = "The Route53 zone id of the ALB to create an alias for"
  default     = ""
}

variable "zone_id" {
  description = "The Route53 zone id of the DNS Domain"
  default     = ""
}
variable "dev_subdomain" {
  description = "Adds dev prefix on subdomains for certificate zoneid ex: *.dev.mmgdev.acuisbackend.com"
  default     = false
}
variable "run_data" {
  description = "Used to switch off data resources when unit testing"
  default     = true
}