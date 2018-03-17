# WeConnect
[![Build Status](https://travis-ci.org/daktari01/we_connect.svg?branch=master)](https://travis-ci.org/daktari01/we_connect)
[![Coverage Status](https://coveralls.io/repos/github/daktari01/we_connect/badge.svg?branch=master)](https://coveralls.io/github/daktari01/we_connect?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/f2f14d50dfbb9dc048ac/maintainability)](https://codeclimate.com/github/daktari01/we_connect/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8e8f3c10e7a340dc868539a377ac1c12)](https://www.codacy.com/app/daktari01/we_connect?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=daktari01/we_connect&amp;utm_campaign=Badge_Grade)

## Introduction
WeConnect is an application where users and busibesses interract. A user is able to create a business profile, from which other users can give reviews about that business.

## The Interface
1. [Home Page](https://daktari01.github.io/we_connect/designs/UI/index.html)
2. [User Registration](https://daktari01.github.io/we_connect/designs/UI/register_user.html)
3. [User Login](https://daktari01.github.io/we_connect/designs/UI/login.html)
4. [Dashbard](https://daktari01.github.io/we_connect/designs/UI/landing_page.html)
5. [Business Profile](https://daktari01.github.io/we_connect/designs/UI/business_profile.html)
  The business profile is where the user can view all reviews or delete a profile
6. [Register business](https://daktari01.github.io/we_connect/designs/UI/register_business.html)
7. Add Review: Click on the "Add Review" button either on the search items returned on the dashboard or on the business profile.
8. [Log Out](https://daktari01.github.io/we_connect/designs/UI/login.html) Takes the user to the login page.

## Getting Started
The following instructions will get you a copy of WeConnect up and running on your local machine for development and testing purposes. 

## Prerequisites
WeConnect application will require the following:   
- A computer running any distribution of Unix or Mac.   
If you are using Windows, liase with your system admin to help you in the installation of WeConnect.
- Python 3.4 or higher   
- Pip
- Git
- Virtualenv

## Installation
1. Clone the repoitory by running the following command on your terminal    
`git clone https://github.com/daktari01/we_connect.git`   
2. Navigate into the project folder   
`cd we_connect`  
3. Create a virtual environment and activate it   
`virtualenv venv`   
`source venv/bin/activate`   
4. Install the requirements   
`pip install -r requirements.txt`   
5. Launch the application   
`python3 run.py`   

## Run The Tests
`nosetests --with-coverage`

## API Endpoints

|URL|HTTP Method|Description|
|:--------|:--------|:-------|
|`/api/auth/register`|POST|Create a user account|
|`/api/auth/login`|POST|Log user in|
|`/api/auth/logout`|POST|Log user out|
|`/api/auth/reset-password`|POST|Reset user password|
|`/api/businesses/`|POST|Register a business|
|`/api/businesses/<businessId>`|PUT|Update a business profile|
|`/api/businesses/<businessId>`|DELETE|Remove a business|
|` /api/businesses/`|GET|Retrieve all businesses|
|`/api/businesses/<businessId>`|GET|Retrieve a business|
|`/api/businesses/<businessId>/reviews`|POST|Add a review for a business|
|`/api/businesses/<businessId>/reviews`|GET|Retrieve (a) review(s) for a business|

## Built With
- Bootstrap 4.0
- Flask RESTful

## How to Contribute
1. Fork the repository to your Github
2. Create a branch
3. Make changes
4. Create a pull request

## Licence
The software is protected under [MIT License](https://opensource.org/licenses/MIT)

## Contributors
- [James Dindi](https://github.com/daktari01)



