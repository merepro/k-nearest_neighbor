from sys import argv
import os.path
import math
import heapq
import copy

#Node class for keeping track of mask values
#and accuracy value
class Node:
  def __init__(self, features = [], accuracy = 0):
    self.features = features
    self.accuracy = accuracy

  #Overload comparator to create a max heap
  def __ge__(self, other):
    return self.accuracy < other.accuracy

#Reads in text file of class instances
#and their respective features, returns a table
#of normalized data values
def getFileInput():
  while True:
    #Open file for reading if it is an actual file
    if len(argv) != 2:
      print "Usage: python nearest_neighbor.py [file_name]"
      exit(1)
    file_input = (argv[1])
    #For each line in the text file, parse spaces and generate
    #table of classes and their respective features
    if os.path.isfile(file_input):
      f = open(file_input, 'rU')
      data_table = []

      for line in f:
        file_line = line.split()
        data_list = []
        for element in file_line:
          #Convert each IEEE-754 floating point into actual number
          data_list.append(float(element))
        data_table.append(data_list)
      #return the table of data
      return data_table
    else:
      print "Invalid file input."

#Fetches user input for algorithm used
def getAlgorithmInput():
  while True:
    print "Type the number of the algorithm you want to run."

    print "\n   1) Forward Selection"
    print "   2) Backward Elimination"
    user_input = raw_input("   3) Hans' Special Algorithm\n\n")
    if user_input == "1":
      algorithmUsed = "ForwardSelection"
      return algorithmUsed
    elif user_input == "2":
      algorithmUsed = "BackwardsElimination"
      return algorithmUsed
    elif user_input == "3":
      algorithmUsed = "SpecialAlgorithm"
      return algorithmUsed

#Performs general search based on user algorithm choice
#Choice 1: Forward selection, start with one feature
#eventually choosing all
#Choice 2: Backwards elimination, start with all features
#eventually choosing one
#Choice 3: (Custom algorithm) Brute force, while using forward
#selection, search entire tree to find best solution
#ALWAYS results in optimal solution
def general_search(algorithmUsed,input_data):
  PQueue = []
  #Dictionary to keep track of visited nodes
  visited = {}
  #Initial max accuracy is unknown
  max_accuracy = -1
  #initial child's max accuracy is unknown
  child_max_accuracy = 0
  heapq.heapify(PQueue)
  data_table = input_data
  root_mask = []
  #Get length of number of features(excluding class ID)
  num_features = len(data_table[0][1:])
  #Flip value for determining forward selection vs
  #backwards elimination
  flip_val = -1

  #Brute force - altered forward selection,
  #searches down with forward selection, then searches rest of tree
  if algorithmUsed == "SpecialAlgorithm":
    print "Using Special Algorithm\n"
    brute_force = 1
    flip_val = 1
    for i in range(0, num_features):
      root_mask.append(0)
  elif algorithmUsed == "ForwardSelection":
    print "Using Forward Selection\n"
    brute_force = 0
    flip_val = 1
    for i in range(0, num_features):
      root_mask.append(0)
  elif algorithmUsed == "BackwardsElimination":
    print "Using Backwards Elimination\n"
    brute_force = 0
    flip_val = 0
    for i in range(0, num_features):
      root_mask.append(1)
  max_accuracy = crossValidation(data_table, root_mask)
  rootNode = Node(root_mask, max_accuracy)

  heapq.heappush(PQueue,rootNode)
  mask_list = []

  #While the queue is not empty, pop
  #the element with the higest accuracy,
  #generate the children for that node,
  #and then proceed to perform cross validation on each child.
  while len(PQueue) != 0:
    prevNode = heapq.heappop(PQueue)
    mask_list = generateMaskChildren(prevNode.features, flip_val)
    for mask_vector in mask_list:
      mask_key = ""
      for elem in mask_vector:
        mask_key += str(elem)

      if mask_key not in visited:
        visited[mask_key] = tuple(mask_vector)
        curr_accuracy = crossValidation(data_table, mask_vector)
        if curr_accuracy >= child_max_accuracy:
          print "\nAccuracy has increased to:", curr_accuracy*100,"%\n"
          child_max_accuracy = curr_accuracy
          child_mask_vector = mask_vector
          nextNode = Node(mask_vector, child_max_accuracy)
          heapq.heappush(PQueue, nextNode)
        #Push node onto heapqu regardless of accuracy if brute force
        #is done
        elif brute_force == 1:
            child_mask_vector = mask_vector
            nextNode = Node(mask_vector, curr_accuracy)
            heapq.heappush(PQueue, nextNode)
    #Check if new child's accuracy is higher than max accuracy, if so
    #update max accuracy.:
    if child_max_accuracy > max_accuracy:
            max_accuracy = child_max_accuracy
            max_mask_vector = child_mask_vector

    #If all child accuracies are lower than max, and brute force is
    #not enabled, stop program and output highest accuracy
    elif brute_force == 0:
      print "Accuracy has decreased for all options, exiting"
      print "Highest accuracy was " , max_accuracy*100,"%" , "using features: { ",
      for x in range(0, len(max_mask_vector)):
        if max_mask_vector[x] == 1:
          print x+1 , " ",
      print "}"
      return

  print brute_force
  print "Special Algorithm finished running."
  print "Higest accuracy was " , max_accuracy*100,"%", "using features: { ",
  for x in range(0, len(max_mask_vector)):
    if max_mask_vector[x] == 1:
      print x+1 , " ",
  print "}"
  return
#Generates children given a parent's mask vector
#and the number of features to flip
#returns a list of children mask vectors
def generateMaskChildren(parent, flip_val):
  child_list = []
  for i in range(0, len(parent)):
      if parent[i] != flip_val:
        child = copy.deepcopy(parent)
        child[i] = flip_val
        child_list.append(child)
  return child_list



#Runs K-nearest neighbor to calculate accuracy for
#a list of class instances
def crossValidation(data_table, mask_vector):
  accuracy = 0
  num_correct = 0
  num_incorrect = 0

  #For each node in node list
  for i in range(0, len(data_table)):
    if max(mask_vector) == 0:
      break
    #Make a copy of the node to be tested
    #Guess the class ID of tested_node
    current_class = nearestNeighbor(data_table, mask_vector, i)
    #Calculate correct and incorrect guesses
    if current_class == data_table[i][0]:
      num_correct += 1
    else:
      num_incorrect += 1

  #Calculate accuracy
  if max(mask_vector) != 0:
    accuracy = float(num_correct) / float(num_incorrect + num_correct)
    print accuracy * 100,"%", "using features: { ",
    for x in range(0, len(mask_vector)):
      if mask_vector[x] == 1:
        print x+1 , "",
    print "}"
    return accuracy
  return 0.0

#Helper function for cross validation
#Calculates nearest neighbor given a modified data table
#where one of the instances is masked
#along with the mask index of the instance
#RETURN: Class ID of tested instance based on nearest neighbor
#mask_vector : A vector of 0 and 1 equating to
#enabled/disabled features
def nearestNeighbor(data, mask_vector, mask_index):
  #If masked index is first element, start default closest at next
  if mask_index == 0:
    nearestNeighborIndex = 1
  #Otherwise default closest value is first element
  else:
    nearestNeighborIndex = 0
  nearestNeighborClass = 0
  #Declare default minimum to be positive infinity
  currentMinimum = float('inf')
  for i in range(0, len(data)):
    euclideanSum = 0
    #Ignore the current neighbor if the element is itself
    if i == mask_index:
      continue
    #Calculate closest neighbor by calculating
    #euclidean distance for each neighbor
    for j in range(1, len(data[i])):
      euclideanSum+= diffOfSquares(data[mask_index][j], data[i][j], mask_vector[j-1])
    euclideanDist = euclideanSum**0.5
    if euclideanDist < currentMinimum:
      currentMinimum = euclideanDist
      nearestNeighborIndex = i
  #return the class of the nearest neighbor
  nearestNeighborClass = data[nearestNeighborIndex][0]
  return nearestNeighborClass

#Calculates mask_value(0 or 1) * (element 1 - element 2)^2
def diffOfSquares(element1, element2, mask_val):
  return float(mask_val) * math.pow(element1-element2,2)

#Main block
def main():
  input_data = getFileInput()
  algorithm = getAlgorithmInput()
  general_search(algorithm , input_data)

#boiler-plate
if __name__ == "__main__":
	main()
