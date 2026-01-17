# -----------------------------------------------------------------------------
# VPC for Database
# -----------------------------------------------------------------------------

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project}-${var.environment}-vpc"
  }
}

# Private Subnets for RDS
resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "${var.project}-${var.environment}-private-${count.index + 1}"
    Type = "private"
  }
}

# -----------------------------------------------------------------------------
# Security Group for RDS
# -----------------------------------------------------------------------------

resource "aws_security_group" "database" {
  name        = "${var.project}-${var.environment}-db-sg"
  description = "Security group for RDS database"
  vpc_id      = aws_vpc.main.id

  # PostgreSQL access from VPC
  ingress {
    description = "PostgreSQL from VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  # MySQL access from VPC (if using MySQL)
  ingress {
    description = "MySQL from VPC"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project}-${var.environment}-db-sg"
  }
}

# -----------------------------------------------------------------------------
# DB Subnet Group
# -----------------------------------------------------------------------------

resource "aws_db_subnet_group" "main" {
  name        = "${var.project}-${var.environment}-db-subnet"
  description = "Database subnet group"
  subnet_ids  = aws_subnet.private[*].id

  tags = {
    Name = "${var.project}-${var.environment}-db-subnet"
  }
}

# -----------------------------------------------------------------------------
# Random Password (if not provided)
# -----------------------------------------------------------------------------

resource "random_password" "db_password" {
  count   = var.db_password == "" ? 1 : 0
  length  = 16
  special = true
  # Exclude characters that cause issues with some databases
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

locals {
  db_password = var.db_password != "" ? var.db_password : random_password.db_password[0].result
}

# -----------------------------------------------------------------------------
# RDS Instance
# -----------------------------------------------------------------------------

resource "aws_db_instance" "main" {
  identifier = "${var.project}-${var.environment}-${var.db_identifier}"

  # Engine
  engine         = var.db_engine
  engine_version = var.db_engine_version

  # Instance
  instance_class = var.db_instance_class

  # Storage
  allocated_storage = var.db_allocated_storage
  storage_type      = var.db_storage_type
  storage_encrypted = true

  # Database
  db_name  = var.db_name
  username = var.db_username
  password = local.db_password

  # Network
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.database.id]
  publicly_accessible    = false
  port                   = var.db_engine == "postgres" ? 5432 : 3306

  # High Availability
  multi_az = var.multi_az

  # Backup
  backup_retention_period = var.backup_retention_period
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"

  # Protection
  deletion_protection = var.deletion_protection
  skip_final_snapshot = var.skip_final_snapshot
  final_snapshot_identifier = var.skip_final_snapshot ? null : "${var.project}-${var.environment}-final-snapshot"

  # Performance
  performance_insights_enabled = var.db_instance_class != "db.t3.micro"

  # Updates
  auto_minor_version_upgrade  = true
  apply_immediately           = var.environment != "prod"
  copy_tags_to_snapshot       = true

  tags = {
    Name = "${var.project}-${var.environment}-${var.db_identifier}"
  }

  lifecycle {
    # Prevent accidental password changes
    ignore_changes = [password]
  }
}
