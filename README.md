# darkbear

the darkbear is a tool to test whether the target server is a honeypot or not.
also, I use [this](https://ro.ecu.edu.au/cgi/viewcontent.cgi?article=1027&context=adf) document for this project.
the document name is "Honeypots: How do you know when you are inside one?".

## create a labratory

you can install the Ubuntu server on a virtual machine or you can use [Cowrie](https://hub.docker.com/r/cowrie/cowrie) in docker.
actually, the Cowrie is a honeypot. so if you want you can pull and run it :

```
docker pull cowrie/cowrie
docker run -p 2222:2222/tcp cowrie/cowrie
```

