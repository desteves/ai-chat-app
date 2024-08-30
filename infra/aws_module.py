"""
_summary_
"""
import pulumi
import pulumi_aws as aws

def declare_aws_resources():
    """_summary_
    """
    # Create a VPC
    vpc = aws.ec2.Vpc(
        'my_cool_vpc',
        cidr_block='10.0.0.0/16',
        tags={
            'Name': 'my-vpc',
        }
    )

    # Create a subnet
    subnet = aws.ec2.Subnet(
        'my_cool_subnet',
        vpc_id=vpc.id,
        cidr_block='10.0.1.0/24',
        tags={
            'Name': 'my-subnet',
        }
    )

    # Create a security group
    security_group = aws.ec2.SecurityGroup(
        'my_cool_security_group',
        vpc_id=vpc.id,
        description='Allow SSH and HTTP',
        ingress=[
            {
                'protocol': 'tcp',
                'from_port': 22,
                'to_port': 22,
                'cidr_blocks': ['0.0.0.0/0'],
            },
            {
                'protocol': 'tcp',
                'from_port': 80,
                'to_port': 80,
                'cidr_blocks': ['0.0.0.0/0'],
            }
        ],
        tags={
            'Name': 'my-security-group',
        }
    )

    # Create an EC2 instance
    user_data = '''#!/bin/bash
    sudo apt-get update -y
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    # Run Docker Compose
    cd /path/to/your/docker-compose-file
    docker-compose up -d
    '''

    instance = aws.ec2.Instance(
        'my_cool_instance',
        instance_type=aws.ec2.InstanceType.T2_MICRO,
        # https://cloud-images.ubuntu.com/locator/ec2/
        ami='ami-01f519a731dd64ba7',  # Replace with a valid AMI ID, amd64/Ubuntu 22.04
        user_data=user_data,
        vpc_security_group_ids=[security_group.id],  # Replace with a valid security group ID
        subnet_id=subnet.id,  # Replace with a valid subnet ID
        associate_public_ip_address=True,
    )

    # Export the public IP address of the instance
    pulumi.export('public_ip', instance.public_ip)
