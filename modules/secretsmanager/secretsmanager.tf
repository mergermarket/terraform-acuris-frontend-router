data "aws_secretsmanager_secret" "secret" {
  count = var.run_data ? 1 : 0
  name  = "tf_fastly_frontend/${var.env == "live" ? "live" : "aslive"}/fastly-to-datadog-api"
}

data "aws_secretsmanager_secret_version" "secret" {
  count     = var.run_data ? 1 : 0
  secret_id = data.aws_secretsmanager_secret.secret[0].id
}
