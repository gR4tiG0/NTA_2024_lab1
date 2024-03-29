# NTA_2024_lab1

TODO:
 - [x] Write code for 
   - [x] Miller-Rabin primality test
   - [x] Trial division method
   - [x] Pollard's rho method 
   - [x] One of Modern Factorization Methods
- [x] Setup docker with listener
- [x] Run tests
- [x] Write lab report


# DOCKER INSTR:
- Download docker image from remote: `docker pull gratigo/nta_lab1:latest`
- Create docker image from git repo: `docker build -t gratigo/nta_lab1 .`
- Start docker container: `docker run --rm -d -p 1337:1337 gratigo/nta_lab1`
- Connect to lab listener: `nc 127.0.0.1 1337`
- Stop docker container: `docker stop $(docker ps | grep "gratigo/nta_lab1" | cut -d " " -f1)`
- To remove image: `docker image rm gratigo/nta_lab1`
