# required
variable "name" {
  description = "The name of the ALB. This name must be unique within your AWS account, can have a maximum of 32 characters"
  type        = string
}

variable "vpc_id" {
  description = "The id of the VPC that the desired security group belongs to"
  type        = string
}

variable "subnet_ids" {
  description = "A list of subnet IDs to attach to the ALB"
  type        = list(string)
}

variable "certificate_domain_name" {
  description = "Domain name as used in AWS ACM Certificate - this will be used by Terraform Data Source to resolve the actual certificate ARN"
  type        = string
}

variable "default_target_group_arn" {
  description = "The ARN of the default Target Group to which to route traffic"
  type        = string
}

# optional
variable "internal" {
  description = "If true, the ALB will be internal"
  type        = string
  default     = "true"
}

variable "extra_security_groups" {
  description = "Extra security groups to be attached to ALB"
  type        = list(string)
  default     = [""]
}

variable "access_logs_bucket" {
  description = "An S3 bucket to send access logs to"
  default     = ""
}

variable "access_logs_enabled" {
  description = "Whether or not to enable access logs"
  default     = false
}

variable "tags" {
  description = "A map of tags to add to all resources"
  default     = {}
}

variable "idle_timeout" {
  description = "The time in seconds that the connection is allowed to be idle."
  type        = string
  default     = "60"
}

variable "run_data" {
  description = "Used to switch off data resources when unit testing"
  default     = true
}

