<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Mastermind</h3>

  <p align="center">
    Implementation test of the Mastermind game for the Inari technical test
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)
* [Testing](#testing)
* [Deployment](#deployment)
* [Built With](#built-with)
* [Contact](#contact)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

1. Clone the repo
```sh
git clone https://github.com/adriantomas/mastermind.git
```
2. Create a virtualenv
3. Install requirements
```sh
pip install -r requirements-dev.txt
```

<!-- USAGE EXAMPLES -->
## Usage

The API is hosted at AWS and available for evaluation through the following endpoints.The base URL is:
```
https://v6w0ihj4fa.execute-api.us-east-1.amazonaws.com/dev/game/9b370d4b-da75-460c-88f4-71040268c710
```

Create a game and return the `game_id`:
```
POST /game
```

Get game info specified by `game_id`:
```
GET /game/:game_id
```

Make an attempt to find out the secret, where `game_id` is the ID of the game and `movement` is a 4 number combination:
```
PUT /game/:game_id/movement/:movement
```

## Testing

Despite not having implemented a large coverage of tests, there are some available. Run:
```sh
pytest
```

## Deployment
It is mandatory to deploy the infrastructure first before the API. To do this, navigate to those infrastructure folders that have a `serverless.yml` and run:

```sh
npm i
serverless deploy
```
After both infrastructure deployments, deploy the API in the same way.


### Built With

* [Python 3.8](https://www.python.org/)
* [Serverless Framework](https://www.serverless.com/)
* [AWS](https://aws.amazon.com/)

<!-- CONTACT -->
## Contact

Adrián Tomás - [dev@adriantomas.com](mailto:dev@adriantomas.com)

Project Link: [https://github.com/adriantomas/mastermind](https://github.com/adriantomas/mastermind)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/adriantomas/repo.svg?style=flat-square
[contributors-url]: https://github.com/adriantomas/mastermind/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/adriantomas/repo.svg?style=flat-square
[forks-url]: https://github.com/adriantomas/mastermind/network/members
[stars-shield]: https://img.shields.io/github/stars/adriantomas/repo.svg?style=flat-square
[stars-url]: https://github.com/adriantomas/mastermind/stargazers
[issues-shield]: https://img.shields.io/github/issues/adriantomas/repo.svg?style=flat-square
[issues-url]: https://github.com/adriantomas/mastermind/issues
[license-shield]: https://img.shields.io/github/license/adriantomas/repo.svg?style=flat-square
[license-url]: https://github.com/adriantomas/mastermind/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/adriantomasvano
