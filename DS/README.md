To use the code in this directory, you will need the semantic space of Baroni et al (2014): Don't count, predict! A systematic comparison of context-counting vs. context-predicting semantic vectors Proceedings of ACL 2014 (52nd Annual Meeting of the Association for Computational Linguistics), East Stroudsburg PA: ACL, 238-247.

**Get the semantic space with:**

`wget http://clic.cimec.unitn.it/composes/materials/EN-wform.w.5.cbow.neg10.400.subsmpl.txt.gz`

`gunzip EN-wform.w.5.cbow.neg10.400.subsmpl.txt.gz`

`mv EN-wform.w.5.cbow.neg10.400.subsmpl.txt ukwac.predict.dm`

**Produce vectors for each document in your corpus:**

`python ./runDistSemWeighted.py example.docs example.docs.dm`

**Produce pear for each user in your evaluation:**

`python ./mkPears.py usernames.txt users.pages.edited.txt`

**Produce profiles for each user:**

`python ./mkProfiles.py usernames.txt`
