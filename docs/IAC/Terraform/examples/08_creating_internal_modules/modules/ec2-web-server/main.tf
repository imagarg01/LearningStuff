# EC2 Web Server Module
#
# This module creates an EC2 instance with company standards:
# - IMDSv2 required (security)
# - EBS encryption enabled
# - Standardized tags
# - Security group with minimal access

# -----------------------------------------------------------------------------
# Data Sources
# -----------------------------------------------------------------------------

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-kernel-6.1-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# -----------------------------------------------------------------------------
# Security Group
# -----------------------------------------------------------------------------

resource "aws_security_group" "this" {
  name        = "${var.name}-sg"
  description = "Security group for ${var.name}"
  vpc_id      = var.vpc_id

  # HTTP access (if web server)
  dynamic "ingress" {
    for_each = var.enable_http ? [1] : []
    content {
      description = "HTTP"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = var.allowed_cidr_blocks
    }
  }

  # HTTPS access (if web server)
  dynamic "ingress" {
    for_each = var.enable_https ? [1] : []
    content {
      description = "HTTPS"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = var.allowed_cidr_blocks
    }
  }

  # SSH access (restricted)
  dynamic "ingress" {
    for_each = var.enable_ssh ? [1] : []
    content {
      description = "SSH"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = var.ssh_allowed_cidr_blocks
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.name}-sg"
  })
}

# -----------------------------------------------------------------------------
# EC2 Instance
# -----------------------------------------------------------------------------

resource "aws_instance" "this" {
  ami                    = var.ami_id != "" ? var.ami_id : data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.this.id]
  key_name               = var.key_name != "" ? var.key_name : null

  # COMPANY STANDARD: IMDSv2 required
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"  # Enforce IMDSv2
    http_put_response_hop_limit = 1
  }

  # COMPANY STANDARD: Encrypted root volume
  root_block_device {
    volume_type           = "gp3"
    volume_size           = var.root_volume_size
    encrypted             = true  # Always encrypted
    delete_on_termination = true
  }

  # User data
  user_data = var.user_data != "" ? base64encode(var.user_data) : null

  # COMPANY STANDARD: Detailed monitoring for production
  monitoring = var.environment == "prod"

  tags = merge(var.tags, {
    Name        = var.name
    Environment = var.environment
  })

  lifecycle {
    # Prevent accidental instance type downgrades in production
    precondition {
      condition     = var.environment != "prod" || !contains(["t3.micro", "t3.nano"], var.instance_type)
      error_message = "Production instances must be t3.small or larger."
    }
  }
}
