# RDS PostgreSQL Module
#
# This module creates an RDS PostgreSQL instance with company standards:
# - Always encrypted
# - Never publicly accessible
# - Minimum backup retention
# - Standard parameter group

# -----------------------------------------------------------------------------
# DB Subnet Group
# -----------------------------------------------------------------------------

resource "aws_db_subnet_group" "this" {
  name        = "${var.name}-subnet-group"
  description = "Subnet group for ${var.name}"
  subnet_ids  = var.subnet_ids

  tags = merge(var.tags, {
    Name = "${var.name}-subnet-group"
  })
}

# -----------------------------------------------------------------------------
# Security Group
# -----------------------------------------------------------------------------

resource "aws_security_group" "this" {
  name        = "${var.name}-db-sg"
  description = "Security group for ${var.name} database"
  vpc_id      = var.vpc_id

  ingress {
    description     = "PostgreSQL from allowed security groups"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = var.allowed_security_group_ids
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.name}-db-sg"
  })
}

# -----------------------------------------------------------------------------
# Random Password
# -----------------------------------------------------------------------------

resource "random_password" "this" {
  count            = var.password == "" ? 1 : 0
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

locals {
  password = var.password != "" ? var.password : random_password.this[0].result
}

# -----------------------------------------------------------------------------
# RDS Instance
# -----------------------------------------------------------------------------

resource "aws_db_instance" "this" {
  identifier = var.name

  # Engine
  engine         = "postgres"
  engine_version = var.engine_version

  # Instance
  instance_class = var.instance_class

  # Storage - COMPANY STANDARD: Always encrypted
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = "gp3"
  storage_encrypted     = true  # MANDATORY

  # Database
  db_name  = var.database_name
  username = var.username
  password = local.password
  port     = 5432

  # Network - COMPANY STANDARD: Never public
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.this.id]
  publicly_accessible    = false  # MANDATORY

  # High Availability
  multi_az = var.multi_az

  # Backup - COMPANY STANDARD: Minimum 7 days
  backup_retention_period = max(var.backup_retention_period, 7)
  backup_window           = var.backup_window
  maintenance_window      = var.maintenance_window

  # Protection
  deletion_protection = var.deletion_protection
  skip_final_snapshot = var.skip_final_snapshot
  final_snapshot_identifier = var.skip_final_snapshot ? null : "${var.name}-final"

  # Monitoring
  performance_insights_enabled = var.instance_class != "db.t3.micro"

  # Updates
  auto_minor_version_upgrade = true
  copy_tags_to_snapshot      = true

  tags = merge(var.tags, {
    Name        = var.name
    Environment = var.environment
  })

  lifecycle {
    # Prevent password changes after creation
    ignore_changes = [password]

    # Prevent deletion without snapshot in production
    precondition {
      condition     = var.environment != "prod" || !var.skip_final_snapshot
      error_message = "Production databases must have final snapshot enabled."
    }
  }
}
