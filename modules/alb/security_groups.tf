locals {
  # open to the world unless access is restricted to managed prefix lists
  ingress_cidr_blocks = length(var.ingress_prefix_list_ids) == 0 ? ["0.0.0.0/0"] : []
}

resource "aws_security_group" "default" {
  vpc_id = var.vpc_id

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    cidr_blocks     = local.ingress_cidr_blocks
    prefix_list_ids = var.ingress_prefix_list_ids
  }

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    cidr_blocks     = local.ingress_cidr_blocks
    prefix_list_ids = var.ingress_prefix_list_ids
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

