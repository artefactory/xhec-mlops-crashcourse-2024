docker build -t nyc_taxi:solution -f Dockerfile.app .
docker run -dp 0.0.0.0:8000:8001 nyc_taxi:solution
