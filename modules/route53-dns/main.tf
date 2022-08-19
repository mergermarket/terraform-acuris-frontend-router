data "aws_route53_zone" "dns_domain" {
  count = var.zone_id == "" ? 1 : 0

  name = local.zone
}

locals {
  zone_id = var.zone_id == "" ? element(data.aws_route53_zone.dns_domain.*.zone_id, 0) : var.zone_id
  zone_prefix = "${var.dev_subdomain && var.env != "live" ? "dev." : ""}"
  zone = "${local.zone_prefix}${var.domain}"
  name = var.env == "live" ? var.name : "${var.env}-${var.name}"
  fqdn = "${local.name}.${local.zone}"
}
resource "aws_route53_record" "dns_record" {
  count = var.alias ? 0 : 1

  zone_id = local.zone_id
  name    = local.fqdn

  type    = "CNAME"
  records = [var.target]
  ttl     = var.ttl

  lifecycle {
    prevent_destroy = true
  }

}

resource "aws_route53_record" "alb_alias" {
  count = var.alias ? 1 : 0

  zone_id = local.zone_id
  name    = local.fqdn
  type    = "A"

  alias {
    name                   = var.target
    zone_id                = var.alb_zone_id
    evaluate_target_health = true
  }

  lifecycle {
    prevent_destroy = true
  }
}
