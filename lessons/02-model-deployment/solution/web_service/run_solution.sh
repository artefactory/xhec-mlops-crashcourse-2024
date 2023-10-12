docker build -t nyc_taxi:solution -f Dockerfile.app .
docker run -p 8000:8001 nyc_taxi:solution
