### /eval directory

Perform the evaluation from this directory. First, make a shared_pears_id file:

`./getSharedPearsIds`

Then, evaluate on a query file. For instance:

`python ./eval.py example.wiki.queries`

(Make sure beforehand that the data you've processed in the DS folder does contain pears with the `correct' pages to be returned for each query, otherwise your evaluation will turn out badly...)
