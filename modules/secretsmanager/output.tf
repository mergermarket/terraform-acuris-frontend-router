output "datadog_api_key" {
  value = "${element(data.aws_secretsmanager_secret_version.secret.*.secret_string, 0)}"
}
