**Produce vectors for each document in your corpus:**

`python ./runDistSemWeighted.py ../data/example.docs example.docs.dm`

**Produce pear for each user in your evaluation:**

`python ./mkPears.py ../data/usernames.txt ../data/users.pages.edited.txt`

**Produce profiles for each user:**

`python ./mkProfiles.py ../data/usernames.txt`
