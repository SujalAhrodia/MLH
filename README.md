# Snap In

## Description
An average internet user has roughly 40 online accounts. That means 40 different username and passwords to remember. But the real problem is to remember different usernames for each website because users usually keep the same passwords for multiple platforms. 

## Introduction
We aim to smoothen user login while making it more secure. It not only removes the entire need of having usernames but also eliminates the need for 2-Layer verification and CAPTCHAs. 

## How we built it
Using Face Recognition we aim to authorize signed up users to log in via their face. We selected the Flask micro web server written in Python and some machine learning models and libraries. We used one-shot learning to train the model. It requires only one image per person to train the model. So, when a user signs up, they enter the information along with an image from the webcam. After that, whenever the user wants to log in, we will scan their face and match the features without a model. The one with the closest set of features, if available, will be prompted and we will ask for their password. If the credentials are right, the user can log in into the system. This is a groundbreaking technology and in the coming time, can act as a replacement for passwords too for the laptops.

## Setup instructions
* Clone the repository and download the depndencies like opencv-python, dblib, flask and face-recognition using `pip`.
* Run the following command:
```
python3 main.py
```

## Challenges we ran into
Frame rendering for Face Recognition was very heavy to perform in real time.

## Accomplishments that we're proud of
Successfully overcame the challenge mentioned above and created a complete web API that is ready to be used by any web service. Other than that, our API doesn't store any actual faces of our users to assure their data privacy. **This was the first project which configures real-time OpenCV face recognization on a web-hosted system.**

## What we learned
We learned about the microservices frameworks and ML libraries. Moreover, we learned about team collaboration and work distribution among peers. This hackathon was a great experience for us and have helped us to learn about many minute concepts as well which might help us in the future IT industry. It also taught us about the societal impacts of the daily efforts by the CS Engineers that prove beneficial.

## What's next for SnapIn
To improve Face Recognition accuracy to distinguish between still images and an actual human.
