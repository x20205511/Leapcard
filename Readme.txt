#Leap Card

Aws account
GitHub account

-To install the packages for this project, please execute the following command,
    pip install -r requirements.txt (Please make sure you are in the same path/directory as that of the requirements.txt file)

Once the packages are installed, try to run the project using the following command -
    python application.py runserver

You will see the application running on your local address. You can browse the website by copy pasting the link in your browser.

However, the website is currently hosted on localhost, that is your own machine.

To deploy the website on public cloud, we are using Amazon Web Services (AWS) Elastic Container (EC2) instance and to implement the CI/CD, we use CodeDeploy and CodePipeline services from AWS.

Make sure you have the following script files under the "scripts" folder - application_stop.sh, before_install.sh, run.sh, validate_service.sh

Create a new IAM Role: EC2 Role for CodeDeploy
    Navigate to AWS, and create a IAM (Identity & Access Management) role -> select type of trusted identity: AWS Service -> Common use cases: EC2 -> Attach permission policies: AmazonEC2RoleforAwsCodeDeploy -> Skip tags -> Create Role: Role name = "EC2_CodeDeploy_Role" -> Click on Create Role.

Create another IAM Role: for CodeDeploy
    Select type of trusted identity: AWS Service -> Under Select your use case: CodeDeploy -> Permission policies: AWSCodeDeployRole -> skip tags -> Role name: CodeDeploy_Role -> Click Create Role.

Create an EC2 instance in AWS,
    Navigate to the EC2 service, click on "Launch instance" -> Choose an Amazon Machine Image (AMI): Ubuntu Server 20.04 LTS (HVM), SSD Volume Type, 64-bit (x86), click on "Select" -> Choose an instance type: "t2.micro" -> Configure instance details: Under "IAM role" drop-down field, select: "EC2_CodeDeploy_Role". In the same step, "Advanced Data", under "User Data": add the following lines,
            #!/bin/bash
            sudo apt update
            sudo apt install ruby
            sudo apt install wget
            cd /home/ubuntu
            wget https://aws-codedeploy-us-east-1.s3.amazonaws.com/latest/install
            sudo chmod +x ./install
            sudo ./install auto
    The above lines are helpful in installing the CodeDeploy service for AWS.
    Further, click on "Add Storage", keep it as-is. -> Click "Tags", "Add Tag", enter the Key name="Name" and value="Leapcard". -> Create Security group, select "Create new security group", click on "Add Rule" and do the following configurations,
        Type: HTTP, Protocol: TCP, Port range: 80
        Type: Custom TCP, Protocol: TCP, Port range: 5000, Source: Anywhere
    Click on "Review and Launch". Create a new Key pair -> Key pair type: RSA -> Key pair name: leapcardkeypair and download the key pair. Click on "Launch instance".

Once the EC2 instance is created, connect to your EC2 instance from your local computer using SSH in Ubuntu terminal. Make sure you copy the keypair file to the home directory, i.e. "~/" in ubuntu and assign appropriate permissions. Now connect with the SSH command which you have copied from AWS. Once you are connected to the EC2 from your Ubuntu terminal, enter the following command to install ruby on EC2 instance,
        ~$ sudo apt install ruby
        ~$ sudo ./install auto - this command will install your CodeDeploy service agent also.
        /opt$ sudo apt install python3-pip
    You will find CodeDeploy agent installed in "/opt" folder. Make sure the "database.db" file has appropriate permissions for EC2 user to perform operations.


Now, navigate to AWS and setup the CodeDeploy service from console,
    Click on "Create application" -> Under "Application Configuration", Application name: "leapcard_devops" and Compute Platform: EC2/On-premises -> Create application.

    Create Deployment groups,
    Click on "Create Deployment group" -> Enter group name: "leapcard_devops_deploymentgroup" -> Service Role: CodeDeploy_Role -> Deployment-type: In-Place -> Enivronment Configuration: Amazon EC2 instances, Enter Key name and value -> Uncheck LoadBalancer.

Create a pipeline using CodePipeline service from AWS Console,
    Enter pipeline name : leapcard_devops_pipeline -> Create new service role -> next.
    Add Source stage: GitHub 2 -> Connect to the github and link your repository.
    Change detection options: Select "Start the pipeline on source code change". Click next.
    Skip build stage.
    Add deploy stage: Deploy provider: CodeDeploy -> Select your region -> Application name -> Deployment group.
    Create pipeline.


Now everytime, there is a change in source code from GitHub, the CI/CD will be executed and the changes will be reflected on our website.