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

# Stored Information

The following information will be stored for each animal:

*Required*
- Name
- Species

*Optional*
- Date of birth (Age automatically calculated)
- Weight
- Height
- Length
- Diet
- Personality
- ID
- Grouping
- Image
- Notes

# How to run tests

I have included a bash script for Mac/Linux which can run the tests for you if you wish without having to manually add or type out environment variables required for testing. 

To allow the file to be ran, run the following:

`chmod +x test`

Then to run the tests, run the following:

`./test`

# Security 

This program is a little project to practice my skills on so do not expect it to be super secure or maintained.

Some basic security will be implemented such as:
- hashing passwords to make it harder to crack.
- using a secret key to encrypt the session cookie.
- using https to encrypt the data sent between the client and server.
- api key will be required to access personal animal data (You can only access your animals or others with permission).

# How to run (Not ready yet)

You can host it locally if you like, it is contained with `docker` so you will need `docker` installed. You can then run the following command to build the image and run it:

```bash
docker build -t animal-tracker
docker run -p 7474:7474 animal-tracker
```

This will then be accessible on `localhost:7474`

# Contribution

I request that you do not contribute to this project as it is a personal project to practice my skills. If you have any suggestions or feedback, please feel free to contact me however as I would love a challenge to add more features or improve it as time goes on (assuming I am learning something new from it).
