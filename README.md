In this project, we built a new solution to put into production the results of the two notebooks from the folder `project_notebook`.

The idea of this solution is to be able to monitor **the level of satistfaction** of the users about the product categories of our e-commerce website, and also to be able to **redirect more efficiently** to the right support channel (if the sentiment is negative), by associating a product category to our user's sentence and storing it in our Firebase database `messages`.

Then we could pretty well imagine our Business Analysts doing the job of looking at things like:
- the global percentage of negative sentiments
- the global percentage of negative sentiments by product category
- the global percentage of negative sentiments by user name and product category
- etc

Of course, the ideal would be to store the cpf of our user, because of the high risk of storing duplicates (name cannot be a primary key), but the idea here is to present a very simplified solution.

***

In this **README** step by step, we assume you've already installed the following virtual environments with `pyenv`
- chatbot
- analise-sentimentos
- http-api-flask
- jupyter-dev

Before to start, you also need to download the BERT model [here](https://drive.google.com/file/d/1d4RBMWwnzFBaPL2TSu-X1lfb3GLv1Pz5/view) and to save it in the following folder: `analise-sentimentos/assets`.

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
cd product-category-classifier-chatbot/chatbot
/Users/pierre.krzisch/.pyenv/versions/3.6.15/envs/chatbot/bin/python app.py
```

# Start the sentiment analysis and product category identifier service
Enter in another terminal:
```bash
cd product-category-classifier-chatbot/analise-sentimentos
`/Users/pierre.krzisch/.pyenv/versions/3.8.12/envs/analise-sentimentos/bin/python app.py`
```

- This service will detect the emotion of the user
    - if the user is angry, then it will inform to redirect to an attende
    - else the chatbot keeps attending our user

In both case it will try to identify the **product category** the user is talking about, and it will save the **message**, the **user name**, the **product category** and the **sentiment** in our Firebase database `messages`.  

The idea is to be able to monitor the level of satistfaction of the users about the product categories of our e-commerce website, and this also allows to redirect more efficiently to the right support channel if the sentiment is negative.


# List database messages result
```bash
cd product-category-classifier-chatbot/http-api
export FLASK_DEBUG=1
/Users/pierre.krzisch/.pyenv/versions/3.10.2/envs/http-api-flask/bin/flask run
```
Then you can request the url in `product-category-classifier-chatbot/http-api/tests.http` if you've installed the [following plugin](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for VS code before. It will list all the messages that have been written in the Firebase database `messages`.


# References
[Pratica devops com docker para machine learning](https://aurimrv.gitbook.io/pratica-devops-com-docker-para-machine-learning/)