# Ward-Visualization
A web service that takes in a League of Legends summoner name and builds a scatter plot graph of ward placement events based around key objectives.

A resource folder should be added with a local.properties file that has the following information:
[global]
api_key=<your Riot Games API key>
solo_queue_id=420

api_key is a property that needs to be set with the key that Riot games provides you with when you create a developer account.
solo_queue_id is a property that, according to the api docs, represents the solo queue id. Any queue can be analyzed, however.
