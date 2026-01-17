# =============================================================================
# VPC Outputs
# =============================================================================

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

# =============================================================================
# Web Server Outputs
# =============================================================================

output "web_instance_id" {
  description = "Web server instance ID"
  value       = module.web_server.instance_id
}

output "web_public_ip" {
  description = "Web server public IP"
  value       = module.web_server.public_ip
}

output "web_url" {
  description = "Web server URL"
  value       = "http://${module.web_server.public_ip}"
}

# =============================================================================
# Database Outputs
# =============================================================================

output "db_endpoint" {
  description = "Database endpoint"
  value       = module.database.endpoint
}

output "db_address" {
  description = "Database address"
  value       = module.database.address
}

output "db_name" {
  description = "Database name"
  value       = module.database.database_name
}

output "db_username" {
  description = "Database username"
  value       = module.database.username
  sensitive   = true
}

output "db_password" {
  description = "Database password"
  value       = module.database.password
  sensitive   = true
}

output "db_connection_string" {
  description = "Database connection string"
  value       = module.database.connection_string
  sensitive   = true
}
