# **Activity**
## **Video Demo**: https://youtu.be/EmWiEikEwQI

## What is Activity?
**Activity** is a Web application made to track your days, it has 3 usages; **Journal, TODO, Timer**.

## Journal
**Journal** is basically like a diary to keep track of your days, you can use it in any way you want, writing your daily progress writing your diary or even to keep some notes. It has a rich text editor as well as a place to input a title, it tracks whatever date it is that you wrote your entry automatically and you can edit it whenever you want as wells as delete your entries.

![Journal Screenshot](/screenshots/Journal.png?raw=true "Journal")

## TODO
It is self explanatory you make to-do lists in which ever style you want with rich text editor and you put a date to-do until date so it's not like journal you actually have to put a date in the future. That's why this application is good to track your past, present and future activity.

![TODO Screenshot] (/screenshots/TODO.png?raw=true "TODO")

## Timer
**Timer** is used to track whatever activity you are doing. For example, we can put reading in a title and put one hour to the timer and at the end of 1 hour it will add that time to the record with the title and date. But if you stop the timer before one hour it will actually count the time passed, for example 10 minutes.

![Timer Screenshot](/screenshots/Timer.png?raw=true "Timer")

![Timer Screenshot](/screenshots/Timer2.png?raw=true "Timer")

### Why Activity?
Activity came from a problem that I had that I wanted to solve is to track whatever it is I'm doing in a day, I have university to keep track of, my hobbies, learning to code and my other activities, so at some point it got hard to keep track of everything, I had written notes on some text file and it wasn't very organized. So I decided why not make a web app and maybe later a mobile app to track whatever it is I'm doing in a day and in an organized way too. I hope to in time make it a mobile app and make it actually a very usable simple application that would help people orginize their days.

### What Is There More To Do:
Actually this isn't the finished app, I wanted to do much more stuff like adding better styling and some other usages. For example, a book reading activity that will get an API of a large book library and you would be able to add any progress that you make on a book. Another think would be adding a location tracker, like places you visited, or want to visit or even keep track of where you been. Like always there is much room to improve maybe in the future I will visit this project and add to it.

### How it works?
Well this is actually pretty simple, I have used sqlite for database and there are 4 tables to track users, journal, to-do list, activity with timer. So whatever you write it goes directly to your data on your user id. timer is a little bit different, I had to use javascript to add functionality to timer to make it count and count the time passed.

#### Challenges Faced and Things Learned:
Since it's my first *real* project I didn't really had a direction with what I was going to do. at first I had some ideas that has something to do with economics model (which I'm currently studying). But I wanted to make something simple to solve a good chunk of my daily problem. So I would say one of the challenges was to get an idea what is it that I can do to solve some problems and be enthusiast about it while doing it.

Next challenge was to actually start, I didn't know how to or where to begin my project. Sure I had ideas but I actually didn't know if I should make html pages first or maybe make all database and leave styling and html at the end. So here is where I made a mistake, I didn't stylize anything until my project was almost finished, and it was a mistake because It got really messy to do everything at the end and if I had to do this project again I would a page at a time with style and functionallity together rather all out finishing project and leaving style and order at the end.

The last challenge was reading documentation, I needed to implement timer and I had to read documentation for javascript and I realized I got impatiant about it and wasted a little bit of time. So now whenever I'm trying to learn from a documentation I'm very patient about it, I learned that if you take a second to let it sink it, it actually really helps you learn.

### For Running On Localhost:
You need to install everything on <code> requirements.text </code> and you have to do <code>flask run</code>.

### Credits:
Navbar: https://github.com/fireship-io/222-responsive-icon-nav-css





