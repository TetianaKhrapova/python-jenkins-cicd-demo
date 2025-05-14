FROM jenkins/inbound-agent:latest

# docker build -t jenkins-custom-agent:1.2 .
USER root

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    ln -sf python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Docker CE
RUN apt-get update && \
    apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure docker group has correct GID (e.g., 999) and add jenkins to it
# RUN DOCKER_GID=998 && \
#     existing_gid=$(getent group docker | cut -d: -f3) && \
#     if [ "$existing_gid" != "$DOCKER_GID" ]; then groupmod -g $DOCKER_GID docker; fi && \
#     usermod -aG docker jenkins
RUN usermod -aG systemd-network jenkins

USER jenkins
