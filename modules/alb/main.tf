data "aws_acm_certificate" "cert" {
  count    = var.run_data ? 1 : 0
  domain   = var.certificate_domain_name
  statuses = ["ISSUED"]
}

resource "aws_alb" "alb" {
  name            = replace(replace(var.name, "/(.{0,32}).*/", "$1"), "/^-+|-+$/", "")
  internal        = var.internal
  security_groups = concat([aws_security_group.default.id], var.extra_security_groups)
  subnets         = var.subnet_ids
  tags            = var.tags
  idle_timeout    = var.idle_timeout

  access_logs {
    bucket  = var.access_logs_bucket
    enabled = var.access_logs_enabled
  }
}

resource "aws_alb_listener" "https" {
  load_balancer_arn = aws_alb.alb.arn
  port              = "443"
  protocol          = "HTTPS"
  certificate_arn   = element(concat(data.aws_acm_certificate.cert.*.arn, [""]), 0)

  default_action {
    target_group_arn = var.default_target_group_arn
    type             = "forward"
  }
}
