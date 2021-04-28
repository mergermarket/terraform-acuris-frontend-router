data "aws_route53_zone" "dns_domain" {
  count = var.zone_id == "" ? 1 : 0

  name = var.dev_subdomain ? data.template_file.domain.rendered : local.zone
}

locals {
  zone_id = var.zone_id == "" ? element(concat(data.aws_route53_zone.dns_domain.*.zone_id, list("")), 0) : var.zone_id
  zone_prefix = "${var.dev_subdomain && var.env != "live" ? "dev." : ""}"
  zone = "${local.zone_prefix}${var.domain}"
  name = "${var.env == "live" ? "" : "${var.env}-"}${var.name}"
  fqdn = "${local.name}.${local.zone}"
  dns_record_name = "${var.env == "live" ? var.name : "${var.env}-${var.name}"}.${data.template_file.domain.rendered}"
}

data "template_file" "domain" {
  template = "$${env == \"live\" ? \"$${domain}\" : \"dev.$${domain}\"}."

  vars = {
    env    = var.env
    domain = var.domain
  }
}

resource "aws_route53_record" "dns_record" {
  count = var.alias ? 0 : 1

  zone_id = local.zone_id
  name    = local.fqdn

  type    = "CNAME"
  records = [var.target]
  ttl     = var.ttl

}

resource "aws_route53_record" "alb_alias" {
  count = var.alias ? 1 : 0

  zone_id = local.zone_id
  name    = var.dev_subdomain ? local.dns_record_name : local.fqdn
  type    = "A"

  alias {
    name                   = var.target
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }
}
