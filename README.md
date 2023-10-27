# animal-tracker

This is a web app which is to be used to keep track of pet information. You can choose to fill in as much or as little information as you like. This information can also be edited or deleted if wanted. I will add an API to the program too so that this data can be accessed by other programs too.

# Features

- [ ] Create an account
- [ ] Login to account
- [ ] Create an animal
- [ ] Edit an animal
- [ ] Delete an animal
- [ ] View all animals
- [ ] Filter list of animals
- [ ] API to access animal data

# Stored Information

The following information will be stored for each animal:

*Required*
- Name
- Species

*Optional*
- Hatch date (Age automatically calculated)
- Weight
- Height
- Length
- Diet
- Personality
- Notes
- Image


# Security 

This program is a little project to practice my skills on so do not expect it to be super secure or maintained.

Some basic security will be implemented such as:
- hashing passwords and using a salt to make it harder to crack.
- using a secret key to encrypt the session cookie.
- using https to encrypt the data sent between the client and server.
- api key will be required to access personal animal data (You can only access your animals or others with permission).

# How to use

This site will be hosted by render on the following link: {tbc}

To access the API, you will need to request your unique api key from the website. This will be sent to you via email and this will need to be included in the request when trying to query data. The API will be hosted on the following link: {tbc}

# How to run (Not ready yet)

You can host it locally if you like, it is contained with `docker` so you will need `docker` installed. You can then run the following command to build the image and run it:

```bash
docker build -t animal-tracker
docker run -p 7474:7474 animal-tracker
```

This will then be accessible on `localhost:7474`

# Contribution

I request that you do not contribute to this project as it is a personal project to practice my skills. If you have any suggestions or feedback, please feel free to contact me however as I would love a challenge to add more features or improve it as time goes on (assuming I am learning something new from it).
