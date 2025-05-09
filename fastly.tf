module "fastly" {
  source = "./modules/fastly-frontend"
  count = var.cloudfront_migrated == "false" ? 1 : 0

  domain_name                 = var.fastly_domain
  additional_domain_names     = var.additional_fastly_domains
  domain_no_prefix            = var.domain_no_prefix
  bare_redirect_domain_name   = var.bare_redirect_domain_name
  backend_address             = module.dns_record.fqdn
  env                         = var.env
  caching                     = var.fastly_caching
  ssl_cert_check              = var.ssl_cert_check
  ssl_cert_hostname           = module.dns_record.fqdn
  force_ssl                   = var.force_ssl
  connect_timeout             = var.connect_timeout
  first_byte_timeout          = var.first_byte_timeout
  between_bytes_timeout       = var.between_bytes_timeout
  custom_vcl_backends         = var.custom_vcl_backends
  custom_vcl_recv             = var.custom_vcl_recv
  custom_vcl_recv_no_shield   = var.custom_vcl_recv_no_shield
  custom_vcl_recv_shield_only = var.custom_vcl_recv_shield_only
  custom_vcl_error            = var.custom_vcl_error
  custom_vcl_deliver          = var.custom_vcl_deliver
  bypass_busy_wait            = var.bypass_busy_wait
  proxy_error_response        = var.proxy_error_response
  not_found_response          = var.not_found_response
  error_response              = var.error_response
  shield                      = var.shield
  surrogate_key_name          = var.surrogate_key_name
  run_data                    = var.run_data
  override_host               = var.override_host
}

