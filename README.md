# bitcoin_containerlized
 
Containerizing the project and then migrating it to the cloud.

1. Create 5 files to connect db
    - crawler/utils/config.py
    - etl/utils/config.py
    - predict/utils/config.py
    - result/utils/config.py
    - charts/utils/config.py

2. Build docker images
    - docker_build.sh

3. Push images to Docker hub
    - docker login
    - push_docker_hub.sh

4. Create cloud vm and use startup script
    - new_azure_machine.sh

5. Confirm that the system migrated successfully
    - bitcoin_containerlized/daily.sh
    - <cloud vm IP>:5000
