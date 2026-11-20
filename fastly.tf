# The Fastly configuration is no longer managed by this module.
#
# This `removed` block tells Terraform to forget every instance of module.fastly
# (including the bare domain redirect service) the next time an apply runs, WITHOUT
# destroying the real Fastly services. No manual `terraform state rm` is needed, and
# the Fastly provider is not called to refresh, plan or update anything.
#
# Consumers that never had Fastly in their state (e.g. cloudfront_migrated = "true")
# are unaffected - the block is a no-op for them.
#
# Once every consumer has applied this version, this file can be deleted.
removed {
  from = module.fastly

  lifecycle {
    destroy = false
  }
}
