# =============================================================================
# VPC Module
# Source: https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws
# =============================================================================

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "${var.project}-${var.environment}"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = [for i, az in var.availability_zones : cidrsubnet(var.vpc_cidr, 8, i + 10)]
  public_subnets  = [for i, az in var.availability_zones : cidrsubnet(var.vpc_cidr, 8, i)]

  # NAT Gateway for private subnets
  enable_nat_gateway     = true
  single_nat_gateway     = var.environment != "prod" # Save costs in non-prod
  one_nat_gateway_per_az = var.environment == "prod"

  # DNS settings
  enable_dns_hostnames = true
  enable_dns_support   = true

  # VPC Flow Logs (optional)
  enable_flow_log                      = false
  create_flow_log_cloudwatch_iam_role  = false
  create_flow_log_cloudwatch_log_group = false

  # Tags for Kubernetes (if needed)
  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }

  tags = {
    Terraform   = "true"
    Environment = var.environment
  }
}

# =============================================================================
# Security Group for ALB
# Source: https://registry.terraform.io/modules/terraform-aws-modules/security-group/aws
# =============================================================================

module "alb_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.1.0"

  name        = "${var.project}-${var.environment}-alb-sg"
  description = "Security group for ALB"
  vpc_id      = module.vpc.vpc_id

  # Ingress rules
  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "https-443-tcp"]

  # Egress rules
  egress_rules = ["all-all"]

  tags = {
    Name = "${var.project}-${var.environment}-alb-sg"
  }
}

# =============================================================================
# Security Group for Application
# =============================================================================

module "app_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.1.0"

  name        = "${var.project}-${var.environment}-app-sg"
  description = "Security group for application"
  vpc_id      = module.vpc.vpc_id

  # Allow traffic from ALB only
  ingress_with_source_security_group_id = [
    {
      from_port                = var.app_port
      to_port                  = var.app_port
      protocol                 = "tcp"
      description              = "App port from ALB"
      source_security_group_id = module.alb_sg.security_group_id
    },
  ]

  # Egress rules
  egress_rules = ["all-all"]

  tags = {
    Name = "${var.project}-${var.environment}-app-sg"
  }
}

# =============================================================================
# Security Group for Database
# =============================================================================

module "db_sg" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.1.0"

  name        = "${var.project}-${var.environment}-db-sg"
  description = "Security group for RDS"
  vpc_id      = module.vpc.vpc_id

  # Allow traffic from app tier only
  ingress_with_source_security_group_id = [
    {
      from_port                = 5432
      to_port                  = 5432
      protocol                 = "tcp"
      description              = "PostgreSQL from app tier"
      source_security_group_id = module.app_sg.security_group_id
    },
  ]

  # Egress rules
  egress_rules = ["all-all"]

  tags = {
    Name = "${var.project}-${var.environment}-db-sg"
  }
}

# =============================================================================
# Application Load Balancer
# Source: https://registry.terraform.io/modules/terraform-aws-modules/alb/aws
# =============================================================================

module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "9.1.0"

  name = "${var.project}-${var.environment}-alb"

  load_balancer_type = "application"

  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.public_subnets

  # Security groups
  security_groups = [module.alb_sg.security_group_id]

  # Disable deletion protection for demo
  enable_deletion_protection = false

  # Listeners
  listeners = {
    http = {
      port     = 80
      protocol = "HTTP"
      forward = {
        target_group_key = "app"
      }
    }
  }

  # Target Groups
  target_groups = {
    app = {
      name_prefix      = "app-"
      protocol         = "HTTP"
      port             = var.app_port
      target_type      = "ip"
      
      health_check = {
        enabled             = true
        interval            = 30
        path                = var.health_check_path
        port                = "traffic-port"
        healthy_threshold   = 3
        unhealthy_threshold = 3
        timeout             = 6
        protocol            = "HTTP"
        matcher             = "200-299"
      }
    }
  }

  tags = {
    Environment = var.environment
  }
}

# =============================================================================
# RDS PostgreSQL
# Source: https://registry.terraform.io/modules/terraform-aws-modules/rds/aws
# =============================================================================

resource "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.3.0"

  identifier = "${var.project}-${var.environment}-db"

  # Engine
  engine               = "postgres"
  engine_version       = "14"
  family               = "postgres14"
  major_engine_version = "14"
  instance_class       = var.db_instance_class

  # Storage
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp3"
  storage_encrypted     = true

  # Database
  db_name  = var.db_name
  username = var.db_username
  password = random_password.db_password.result
  port     = 5432

  # Network
  db_subnet_group_name   = module.vpc.database_subnet_group_name
  vpc_security_group_ids = [module.db_sg.security_group_id]
  publicly_accessible    = false

  # Multi-AZ
  multi_az = var.environment == "prod"

  # Maintenance
  maintenance_window              = "Mon:00:00-Mon:03:00"
  backup_window                   = "03:00-06:00"
  backup_retention_period         = var.environment == "prod" ? 30 : 7
  skip_final_snapshot             = var.environment != "prod"
  deletion_protection             = var.environment == "prod"
  performance_insights_enabled    = var.db_instance_class != "db.t3.micro"
  auto_minor_version_upgrade      = true
  apply_immediately               = var.environment != "prod"

  # Parameter group
  parameters = [
    {
      name  = "log_connections"
      value = "1"
    },
    {
      name  = "log_disconnections"
      value = "1"
    }
  ]

  tags = {
    Environment = var.environment
  }
}

# =============================================================================
# Data Sources
# =============================================================================

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
