# =============================================================================
# ROOT MODULE
# 
# This is how developers in your organization would use the internal modules.
# They don't need to know how VPC, EC2, or RDS work internally - they just
# call the pre-approved modules with their configuration.
# =============================================================================

locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# =============================================================================
# NETWORKING
# Using internal VPC module
# =============================================================================

module "vpc" {
  source = "./modules/vpc"

  name               = "${var.project}-${var.environment}"
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  enable_nat_gateway = var.environment != "dev"  # Save costs in dev

  tags = local.common_tags
}

# =============================================================================
# WEB SERVER
# Using internal EC2 module
# =============================================================================

module "web_server" {
  source = "./modules/ec2-web-server"

  name          = "${var.project}-${var.environment}-web"
  vpc_id        = module.vpc.vpc_id
  subnet_id     = module.vpc.public_subnet_ids[0]
  environment   = var.environment
  instance_type = var.web_instance_type

  # Web server settings
  enable_http  = true
  enable_https = false
  enable_ssh   = var.environment == "dev"

  # SSH only from VPC in dev
  ssh_allowed_cidr_blocks = var.environment == "dev" ? [var.vpc_cidr] : []

  # User data to install web server
  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y httpd
    systemctl start httpd
    systemctl enable httpd
    echo "<h1>Hello from ${var.environment}!</h1>" > /var/www/html/index.html
    echo "<p>Instance: $(curl -s http://169.254.169.254/latest/meta-data/instance-id)</p>" >> /var/www/html/index.html
  EOF

  tags = local.common_tags
}

# =============================================================================
# DATABASE
# Using internal RDS module
# =============================================================================

module "database" {
  source = "./modules/rds-postgres"

  name                       = "${var.project}-${var.environment}-db"
  vpc_id                     = module.vpc.vpc_id
  subnet_ids                 = module.vpc.private_subnet_ids
  allowed_security_group_ids = [module.web_server.security_group_id]
  environment                = var.environment

  # Database settings
  instance_class = var.db_instance_class
  database_name  = var.db_name

  # Environment-specific settings
  multi_az            = var.environment == "prod"
  deletion_protection = var.environment == "prod"
  skip_final_snapshot = var.environment != "prod"

  tags = local.common_tags
}
