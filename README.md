k-nearest_neighbor
==================

This is an implementation of the k-nearest neighbor classifer algorithm.
The algorithm is able to train data sets through the use of cross-validation,
and uses the euclidean distance as a distance metric for finding the nearest
neighbor.

In this implementation k is set to 1, and the searches used for finding 
efficient and accurate classifications are forward selection and
backwards elimination. An exhaustive search is also available, however
highly unadvised as the runtime for even a medium data set of 
1000 instances and 20 features is upwards of 1 hour and 30 minutes.

Test cases are restricted to 2 classes, with up to 1000 instances. The 
maximum number of features used is 40.

To run the program, simply type:

    python nearest_neighbor.py [data-set.txt]

then follow the prompts to select the search algorithm
