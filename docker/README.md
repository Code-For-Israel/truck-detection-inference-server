
# Launch an instance in AWS
1. Connect to AWS waste-reduction account
2. Create a new EC2 instance from the `Launch instances` wizard
   1. Give it a name
   2. Click `Browse more AMIs`
   3. In search bar search for `ami-013d3da30d7c5977d` and choose from `Community AMIs` - Deep Learning Base AMI (Ubuntu 18.04) Version 55.0 (press `Select`)
   4. Instance type: `g4dn.xlarge`
   5. Key pair - choose the `ireland-eu-west-1-waste-reduction-key.pem`
   6. Allow all network traffics
      1. Allow SSH traffic from
      2. Allow HTTPS traffic from the internet
      3. Allow HTTP traffic from the internet
   7. Choose 128GB
   8. Press `Launch instance`
9. To log in to the instance use: `ssh -i ireland-eu-west-1-waste-reduction-key.pem ubuntu@<instance_public_ip>`


```bash
git clone https://github.com/Code-For-Israel/truck-detection-inference-server.git
 
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user

sudo systemctl enable /usr/lib/systemd/system/docker.service

scp -i ireland-eu-west-1-waste-reduction-key.pem -r app ec2-user@ec2-52-18-97-138.eu-west-1.compute.amazonaws.com:/home/ec2-user

cd app
docker build -t myapp .

Auto start container on instance’s boot (example):
$ docker run --restart=always -p 80:80 myapp

```