# Speak & Share
### A Web Application for Language Exchange and Connecting
## Description:
#### What is Speak and Share
Speak & Share offers a platform where users can post announcements to find language partners. Users have the opportunity to browse through others' posts, facilitating meaningful connections with fellow language enthusiasts.

#### Features
1. Create an account to post your own announcement.
2. Search through other posts, filtering by the languages spoken or learned, and by the country of residence.
3. Delete your own post at any time.
4. Communicate with other users by sending messages. Check your received messages in the Messages category.
5. Save posts that interest you to revisit later in the Saved category.
6. On the homepage, discover the top three most popular languages users want to learn on the website, as well as the locations with the highest number of learners.

#### Technologies Used
* Python: The project's robust backend is powered by Python, offering scalability, reliability, and efficiency in data processing and management.
* Flask: Leveraging the Flask web framework, the project ensures seamless integration of various components, simplifying routing, request handling, and overall web application development.
* Bootstrap: Utilizing Bootstrap, the project guarantees a visually appealing and user-friendly interface across different devices, thanks to its responsive design features and extensive library of pre-designed components.
* HTML: Employed for structuring the web pages, provides the foundation for presenting content in a clear and organized manner.
* JavaScript: Enhancing user experience and adding interactivity to the web pages, JavaScript plays a crucial role in implementing dynamic elements, form validation, and asynchronous communication with the server.
* D3.js: Empowering the project with dynamic and interactive data visualizations, D3.js facilitates the creation of pie charts enabling users to gain insights from complex datasets with ease.

#### Project Structure
```
project
 ┣ flask_session        -Flask extension
 ┃
 ┣ static
 ┃ ┣ explore.js         -Javascript funtions for explore.html（pagination of posts,
 ┃ ┃                     filters, liking, saving posts and sending messages to users）
 ┃ ┃
 ┃ ┣ png                -Image resources for the entire website
 ┃ ┗ styles.css         -Adjust error message's style
 ┃
 ┣ templates
 ┃ ┣ edit-profile.html  -Page that allow users to edit profile(email and country)
 ┃ ┣ error.html         -Page will show server errors
 ┃ ┣ explore.html       -Page that allow users to browse and filter other users'
 ┃ ┃                     posts（link to explore.js）
 ┃ ┃
 ┃ ┣ home.html          -Home page showing the most popular languages according to
 ┃ ┃                     the database on this website(D3.js creates the charts)
 ┃ ┃
 ┃ ┣ layout.html        -The layout for entire web using Bootstrap style class
 ┃ ┣ login.html         -Page that allow users to login with username and password
 ┃ ┣ messages.html      -Page that displays messages received by users and allows
 ┃ ┃                     to reply to the sender
 ┃ ┃
 ┃ ┣ post.html          -Page allowing users to post language exchange partner
 ┃ ┃                     announcements
 ┃ ┃
 ┃ ┣ profile.html       -This page will be displayed after successful login
 ┃ ┣ register.html      -Page that allow users to sign up a new account
 ┃ ┣ saved.html         -This page displays the user's favorite posts
 ┃ ┃                     (here they can unsave posts or send a message to the post owner)
 ┃ ┗
 ┃
 ┣ requirements.txt     -file used by Heroku to understand packages
 ┣ app.py               -Main python file（Define route, fetch data between javascript）
 ┣ helpers.py           -Includes functions that can handle error messages, routing
 ┃                       decorations required for logging in, and email format checking
 ┃
 ┣ langex.db            -Database storing users, posts, messages and counties and languages
 ┗ README.md
 ```
#### Running locally
```
$ flask run
```
#### [Video Demo]:
 (https://youtu.be/cWwkSuPm7hg)
