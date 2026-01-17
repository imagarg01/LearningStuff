#!/bin/bash
# Cleanup script for Basic VPC

set -e

if [ ! -f .vpc-ids ]; then
    echo "No .vpc-ids file found. Nothing to clean up."
    exit 0
fi

source .vpc-ids

echo "Cleaning up VPC resources..."

# Delete route table associations and routes
ASSOC_IDS=$(aws ec2 describe-route-tables \
    --route-table-ids $RTB_ID \
    --query 'RouteTables[0].Associations[?!Main].RouteTableAssociationId' \
    --output text 2>/dev/null || echo "")

for ASSOC_ID in $ASSOC_IDS; do
    echo "Disassociating route table: $ASSOC_ID"
    aws ec2 disassociate-route-table --association-id $ASSOC_ID 2>/dev/null || true
done

# Delete route table
echo "Deleting route table: $RTB_ID"
aws ec2 delete-route-table --route-table-id $RTB_ID 2>/dev/null || true

# Delete subnets
echo "Deleting subnet: $SUBNET_1_ID"
aws ec2 delete-subnet --subnet-id $SUBNET_1_ID 2>/dev/null || true

echo "Deleting subnet: $SUBNET_2_ID"
aws ec2 delete-subnet --subnet-id $SUBNET_2_ID 2>/dev/null || true

# Detach and delete internet gateway
echo "Detaching internet gateway: $IGW_ID"
aws ec2 detach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID 2>/dev/null || true

echo "Deleting internet gateway: $IGW_ID"
aws ec2 delete-internet-gateway --internet-gateway-id $IGW_ID 2>/dev/null || true

# Delete VPC
echo "Deleting VPC: $VPC_ID"
aws ec2 delete-vpc --vpc-id $VPC_ID 2>/dev/null || true

# Remove IDs file
rm -f .vpc-ids

echo "Cleanup complete!"
