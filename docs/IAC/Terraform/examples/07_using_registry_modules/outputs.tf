# =============================================================================
# VPC Outputs
# =============================================================================

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = module.vpc.vpc_cidr_block
}

output "public_subnets" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnets
}

output "private_subnets" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnets
}

output "database_subnets" {
  description = "Database subnet IDs"
  value       = module.vpc.database_subnets
}

output "nat_gateway_ips" {
  description = "NAT Gateway public IPs"
  value       = module.vpc.nat_public_ips
}

# =============================================================================
# Security Group Outputs
# =============================================================================

output "alb_security_group_id" {
  description = "ALB security group ID"
  value       = module.alb_sg.security_group_id
}

output "app_security_group_id" {
  description = "Application security group ID"
  value       = module.app_sg.security_group_id
}

output "db_security_group_id" {
  description = "Database security group ID"
  value       = module.db_sg.security_group_id
}

# =============================================================================
# ALB Outputs
# =============================================================================

output "alb_arn" {
  description = "ALB ARN"
  value       = module.alb.arn
}

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = module.alb.dns_name
}

output "alb_zone_id" {
  description = "ALB Zone ID (for Route53)"
  value       = module.alb.zone_id
}

output "application_url" {
  description = "Application URL"
  value       = "http://${module.alb.dns_name}"
}

# =============================================================================
# RDS Outputs
# =============================================================================

output "db_instance_id" {
  description = "RDS instance ID"
  value       = module.rds.db_instance_identifier
}

output "db_instance_endpoint" {
  description = "RDS instance endpoint"
  value       = module.rds.db_instance_endpoint
}

output "db_instance_address" {
  description = "RDS instance address"
  value       = module.rds.db_instance_address
}

output "db_instance_port" {
  description = "RDS instance port"
  value       = module.rds.db_instance_port
}

output "db_name" {
  description = "Database name"
  value       = module.rds.db_instance_name
}

output "db_username" {
  description = "Database master username"
  value       = module.rds.db_instance_username
  sensitive   = true
}

output "db_password" {
  description = "Database master password"
  value       = random_password.db_password.result
  sensitive   = true
}

# =============================================================================
# Connection Strings (for applications)
# =============================================================================

output "database_connection_string" {
  description = "PostgreSQL connection string"
  value       = "postgresql://${module.rds.db_instance_username}:<password>@${module.rds.db_instance_endpoint}/${module.rds.db_instance_name}"
  sensitive   = true
}

# =============================================================================
# Account Info
# =============================================================================

output "aws_account_id" {
  description = "AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "AWS Region"
  value       = data.aws_region.current.name
}
