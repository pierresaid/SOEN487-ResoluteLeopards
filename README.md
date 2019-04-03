# SOEN487-ResoluteLeopards

## Description
_CatVSDog.com_ will finally answer the question we all have: 
_Who is cuter between cats and dogs?_ 🐈 🐩

As the meme war between dogs owners and cats owners rages on, this question is important, more than ever.

Create an account within seconds on our awesome web application, and instantly start scrolling through the feed of cute pet pictures.
Vote for your favorite one! 💖

Each member can also start a duel by generating a post with which others will be able to interact. 💯

Finally, thanks to our statistics page and API, you'll be able to see which pet is the favorite one in real time! 📊

### Technical description

#### Micro-services (back-end)

To make the whole system work, we are providing several APIs:
- ``USER API``: Is handling the users of the application. Allows them to log in, log out, create, edit and delete their profile.
Requirements:
    - Password validation and JWT creation
    - Security, via flask packages
- ``IMAGE FETCHING API``: Retrieves the cutest dog and cat pictures of the web.
Requirements:
    - Abstraction of foreign APIs that return random pictures of cats and dogs. Provides 2 methods: GetCatPicture and GetDogPicture.
- ``FACE-OFF API``: Interacts with the image fetching service to build a duel between a dog and a cat. Then, creates a post that will pop up in the users' feeds. It handles the votes and sends them to the DB service.
Requirements:
    - Retrieve posts by date (order by)
    - Retrieve post by ID
    - Generate a match opposing a cat and a dog, with the initialization of a counter.
    - Store the post in DB
    - Send votes as long as the post is active.
- ``ANALYTICS API``: Computes the global score for dogs and cats from the votes. It keeps the dedicated page updated with the answer to the big question: "Who's cuter between cats and dogs ?"
Requirements:
    - Compute the votes and compile various statistics.

These micro-services are developed using __Flask__ and various external packages, for specific features (JWT management, CORS requests, etc.).

#### Front-end

The APIS are used by the front-end of our application, which is developed using the javascript framework __Vue.js__.

## Installation

## Execution
* On unix
    * Launch all API's and web ap with : ./launch
    * To kill all processes : ./killall


## Contributors

| Name | Email address | Student ID |
|------|---------------|------------|
| Pierre Said | pierre.said@epitech.eu | 40102552 |
| Guillaume Hitier | guillaume.hitier@epitech.eu | 40102556 |
| Clément Peau | clement.peau@epitech.eu | 40102553 |
| Theo Penavaire | theo.penavaire@epitech.eu | 40102474 |

## Tasks

#### Pierre Saïd 
- task 1
- task 2
- etc

#### Guillaume Hitier
- task 1
- task 2
- etc

#### Clément Peau
- task 1
- task 2
- etc

#### Theo Penavaire 
- Image Fetching API development
- task 2
- etc

## Misc.
