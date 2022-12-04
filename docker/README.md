# Launch an instance in AWS

1. Connect to AWS waste-reduction account
2. Create a new EC2 instance from the `Launch instances` wizard
    1. Give it a name
    2. Click `Browse more AMIs`
    3. In search bar search for `ami-013d3da30d7c5977d` and choose from `Community AMIs` - Deep Learning Base AMI (
       Ubuntu 18.04) Version 55.0 (press `Select`)
    4. Instance type: `g4dn.xlarge`
    5. Key pair - choose the `ireland-eu-west-1-waste-reduction-key.pem`
    6. Allow all network traffics
        1. Allow SSH traffic from
        2. Allow HTTPS traffic from the internet
        3. Allow HTTP traffic from the internet
    7. Choose 128GB
    8. Press `Launch instance`
3. To log in to the instance use: `ssh -i ireland-eu-west-1-waste-reduction-key.pem ubuntu@<instance_public_ip>`

# Build docker image

```bash
# Clone git repo
git clone https://github.com/Code-For-Israel/truck-detection-inference-server.git
 
# Build docker image
cd truck-detection-inference-server/docker
sudo docker build -t trucks-inference-server-docker-image .
```

# Export docker image and upload to s3

```bash
sudo docker save trucks-inference-server-docker-image:latest | gzip > trucks_inference_server_docker_image.tar.gz
sudo aws s3 cp trucks_inference_server_docker_image.tar.gz.tar.gz <some s3 path>
```

# Run docker image

```bash
cd truck-detection-inference-server
sudo docker run -d -it \
    --name trucks-inference-server-docker-container \
    --volume $(pwd):/code \
    --net=host \
    --restart unless-stopped \
    --runtime=nvidia \
    --entrypoint "/bin/bash" trucks-inference-server-docker-image:latest \
    -c "chmod +x docker-startup.sh && ./docker-startup.sh"
    
# TODO YOTAM: ADD uWSGI
```

# Run commands inside container
```bash
sudo docker exec -ti trucks-inference-server-docker-container sh
```

# Example calling the docker
```bash
# from the EC2 hosting the docker
curl -X GET http://localhost:5000/detect_trucks

# from anywhere else
curl -X GET http://<public_ip_ec2_hosting_docker>:5000/detect_trucks
```
