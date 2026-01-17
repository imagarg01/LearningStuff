# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------

output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.this.id
}

output "instance_arn" {
  description = "EC2 instance ARN"
  value       = aws_instance.this.arn
}

output "private_ip" {
  description = "Private IP address"
  value       = aws_instance.this.private_ip
}

output "public_ip" {
  description = "Public IP address (if applicable)"
  value       = aws_instance.this.public_ip
}

output "public_dns" {
  description = "Public DNS name"
  value       = aws_instance.this.public_dns
}

output "security_group_id" {
  description = "Security group ID"
  value       = aws_security_group.this.id
}

output "ami_id" {
  description = "AMI ID used"
  value       = aws_instance.this.ami
}
