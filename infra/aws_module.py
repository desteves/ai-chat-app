"""
_summary_
"""
import os
import pulumi
import pulumi_aws as aws

def declare_aws_resources():
    """_summary_
    """
    # Create a VPC
    vpc = aws.ec2.Vpc(
        'my_cool_vpc',
        cidr_block='10.0.0.0/16',
        enable_dns_hostnames=True,
        enable_dns_support=True,
        tags={
            'Name': 'my-cool-vpc',
        }
    )

    # Create an Internet Gateway
    igw = aws.ec2.InternetGateway(
        "my_cool_igw",
        vpc_id=vpc.id,
        tags={
            'Name': 'my-cool-igw',
        }
    )

    # Create a Route Table
    route_table = aws.ec2.RouteTable(
        "my_cool_route_table",
        vpc_id=vpc.id,
        routes=[{
            'cidr_block': "0.0.0.0/0",
            'gateway_id': igw.id,
        }],
        tags={
            'Name': 'my-cool-routetable',
        }
    )

    # Create a subnet
    subnet = aws.ec2.Subnet(
        'my_cool_subnet',
        vpc_id=vpc.id,
        cidr_block='10.0.1.0/24',
        map_public_ip_on_launch=True,
        tags={
            'Name': 'my-cool-subnet',
        }
    )

    # Associate the Route Table with the Subnet
    route_table_association = aws.ec2.RouteTableAssociation(
        "my-route-table-association",
        subnet_id=subnet.id,
        route_table_id=route_table.id,
        tags={
            'Name': 'my-cool-rta',
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
                'cidr_blocks': ['18.237.140.160/29'], # us-west-2 limited
            },
            {
                'protocol': 'tcp',
                'from_port': 80,
                'to_port': 80,
                'cidr_blocks': ['0.0.0.0/0'],
            }
        ],
        egress=[
            {
                'protocol': "-1",
                'from_port': 0,
                'to_port': 0,
                'cidr_blocks': ["0.0.0.0/0"],
            }
        ],
        tags={
            'Name': 'my-cool-security-group',
        }
    )

    pulumi_access_token = os.getenv("PULUMI_TEAM_TOKEN_EC2_ESC")
    # Create an EC2 instance
    # cat /var/log/cloud-init-output.log
    user_data = f'''#!/bin/bash
    # Set up dependencies
    echo "user_data SCRIPT_LOG_START"
    sudo apt-get update -y
    sudo apt-get install -y docker.io git
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Set up the repo
    git clone https://github.com/desteves/ai-chat-app.git /home/ubuntu/repo
    cd /home/ubuntu/repo/app
    
    # Set environment variables with Pulumi ESC
    curl -fsSL https://get.pulumi.com/esc/install.sh | sh
    export PULUMI_ACCESS_TOKEN={pulumi_access_token}
    export PULUMI_ESC_ENV=my-cool-chat-app-env
    /.pulumi/bin/esc env open $PULUMI_ESC_ENV --format dotenv > ./web/.env
    /.pulumi/bin/esc env open $PULUMI_ESC_ENV --format dotenv > ./api/.env
    unset PULUMI_ACCESS_TOKEN
    # Run Docker Compose
    sed -i 's/8888:/80:/g' docker-compose.yml
    docker-compose up
    sudo ufw allow 80/tcp
    '''

    instance = aws.ec2.Instance(
        'my_cool_instance',
        instance_type=aws.ec2.InstanceType.T2_MICRO,
        # https://cloud-images.ubuntu.com/locator/ec2/
        ami='ami-01f519a731dd64ba7',  # Replace with a valid AMI ID, amd64/Ubuntu 22.04
        user_data=user_data,
        user_data_replace_on_change=True,
        vpc_security_group_ids=[security_group.id],  # Replace with a valid security group ID
        subnet_id=subnet.id,  # Replace with a valid subnet ID
        associate_public_ip_address=True,
        tags={
            'Name': 'my-cool-instance',
        },
        # Ensure the instance is created only after the route table association is created
        # This is to ensure that the instance can communicate with the internet
        # thus the user_data script can successfully run
        opts=pulumi.ResourceOptions(
            depends_on=[route_table_association]),
    )

    pulumi.export('url', f'http://{instance.public_ip}:80')
