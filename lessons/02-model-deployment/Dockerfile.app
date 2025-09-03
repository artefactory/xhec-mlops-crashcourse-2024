FROM python:3.11.6-slim
##### Enter your code here #####
# You can find A LOT of resources on the internet (good example: https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/)
# Don't forget to :
# - Install the app dependencies
#   - Install pip on the container
#   - Copy your dependencies (written in a txt file, look at pip-compile package)
#   - Run the pip command
# - Expose the correct port
# - Copy your files in the container
WORKDIR /web_service
# - Initialize the app with uvicorn
