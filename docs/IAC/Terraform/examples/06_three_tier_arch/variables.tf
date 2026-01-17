# -----------------------------------------------------------------------------
# General Variables
# -----------------------------------------------------------------------------

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "project" {
  description = "Project name"
  type        = string
  default     = "three-tier-app"
}

# -----------------------------------------------------------------------------
# VPC Configuration
# -----------------------------------------------------------------------------

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# -----------------------------------------------------------------------------
# Web Tier Configuration
# -----------------------------------------------------------------------------

variable "web_instance_type" {
  description = "Instance type for web servers"
  type        = string
  default     = "t3.micro"
}

variable "web_min_size" {
  description = "Minimum number of web servers"
  type        = number
  default     = 1
}

variable "web_max_size" {
  description = "Maximum number of web servers"
  type        = number
  default     = 4
}

variable "web_desired_size" {
  description = "Desired number of web servers"
  type        = number
  default     = 2
}

# -----------------------------------------------------------------------------
# Application Tier Configuration
# -----------------------------------------------------------------------------

variable "app_instance_type" {
  description = "Instance type for app servers"
  type        = string
  default     = "t3.micro"
}

variable "app_min_size" {
  description = "Minimum number of app servers"
  type        = number
  default     = 1
}

variable "app_max_size" {
  description = "Maximum number of app servers"
  type        = number
  default     = 4
}

variable "app_desired_size" {
  description = "Desired number of app servers"
  type        = number
  default     = 2
}

# -----------------------------------------------------------------------------
# Database Tier Configuration
# -----------------------------------------------------------------------------

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_engine" {
  description = "Database engine"
  type        = string
  default     = "postgres"
}

variable "db_engine_version" {
  description = "Database engine version"
  type        = string
  default     = "14"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
  default     = ""
}

variable "db_allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 20
}

variable "db_multi_az" {
  description = "Enable Multi-AZ deployment"
  type        = bool
  default     = false
}

variable "skip_final_snapshot" {
  description = "Skip final snapshot on destroy"
  type        = bool
  default     = true
}

# -----------------------------------------------------------------------------
# SSH Access
# -----------------------------------------------------------------------------

variable "key_name" {
  description = "SSH key pair name"
  type        = string
  default     = ""
}
