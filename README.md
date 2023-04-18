# ai-text-detection

This application was created to check if the text was generated by artificial intelligence or written by a human.

To develop this application, a data set of 35,000 texts written by people and ChatGPT was used, which were converted into 20 numerical values ​​that describe their characteristics.

The following configuration was used to generate texts in ChatGpt

```
model="text-curie-001"
prompt=prompt
temperature=0.7
max_tokens=300
top_p=1
frequency_penalty=0.4
presence_penalty=0.1
```

### How to run app:
1) Build app
```
> docker-compose up --build
```

And open http://127.0.0.1:8010/

1) Open your Cloud Service Portal and create the new Deployment
2) Go to configuration page in the app and set your deployment credentials
3) In the Cloud Service Portal open "Add and Manage files" page and add GPT-human-text.csv from the /data folder
4) Open the "Import files" page and import current file to the Texts table
5) Then go to "IntegratedML Tools" and create and train a new model "TextModel" with the name of the training model "TextTrainedModel"
5) Go back to the application, enter your text and look at the result. (The maximum text length is 2500 characters)


