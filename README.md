In this README step by step, we suppose you already have installed the following virtual environments with `pyenv`
- chatbot
- analise-sentimentos

Else, you can follow the [guideline](https://aurimrv.gitbook.io/pratica-devops-com-docker-para-machine-learning/2-desenvolvimento/2-1-do-notebook-para-aplicacao-parte-1) of this [book](https://aurimrv.gitbook.io/pratica-devops-com-docker-para-machine-learning/).

# Services initialization
Start the ZooKeeper service:
```bash
# Start the ZooKeeper service
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Open another terminal session and run:
```bash
# Start the Kafka broker service
bin/kafka-server-start.sh config/server.properties
```

# Start the chatbot thread
Enter in another terminal:
```bash
cd eml1-at2/chatbot
/Users/pierre.krzisch/.pyenv/versions/3.6.15/envs/chatbot/bin/python app.py
```

# Start the sentiment analysis and product category identifier service
Enter in another terminal:
```bash
cd eml1-at2/analise-sentimentos
/Users/pierre.krzisch/.pyenv/versions/3.8.12/envs/analise-sentimentos/bin/python app.py
```

- This service will detect the emotion of the user
    - if the user is angry, then it will inform to redirect to an attende
    - else the chatbot keeps attending our user

In both case it will try to identify the **product category** the user is talking about, and it will save the **message**, the **user name**, the **product category** and the **sentiment** in our Firebase database `messages`.  

The idea is to be able to monitor the level of satistfaction of the users about the product categories of our e-commerce website, and this also allows to redirect more efficiently to the right support channel if the sentiment is negative.
