#North Fantasy
##Project Description
This is a lightweight Django (4.1) web application that can be used to run your own custom Fantasy League for your local football team. 

It was born out of a personal need where our football team was running a custom Fantasy League for our Friday night soccer games. The use of multiple spreadsheets was getting convoluted and as such this applicatin was born.

##Features
Basic features include the ability to input a position for each player for each round and then select which player scored points for each rule. 

An additional field on League Rules is the ```required_forms``` which will display x amount of forms when inputting points, as some rules more people are likely to score, for example, attending a game, while some will be less, for example, scoring a goal.

Other additional features include the ability to adjust points based on the position, allowing you to award more points for a defender scoring a goal, as an example and the ability to see all goals, assists and individual points for the season and individual rounds.
##Setup
To run the project locally, simply clone this repository and ```run docker compose up```

The project will then spin up two containers, one for running the Django application with runserver and another to host the Postgres Server for the database. 

You will then have to create a League, your league rules and input your players and rounds via their respective tables.  For now there is no CRUD pages for these records so I recommend using the Django admin.

Keep in mind, when creating your League record you will have to associate it with a user record as an admin so you can actually add points to your players. For the time being I recommend using ```manage.py createsuperuser```
##Development Roadmap
There are quite a few features that are planned for development, however currently the application is use usable as a way to track everyone's points.

Upcoming next will be the ability to view "Player Profiles", including detailed breakdowns of a players points across the season and for each round. 

Following this, adding the CRUD functionality within the app itself for League administrators for Rules and Players.

Custom positions per league is also on the roadmap as this will allow the application to be used outside the context of a football team.

We'll probably also add a nice marketable homepage and some basic functionality to search for and view all League's, just so players have an easy way to find what they are looking for.