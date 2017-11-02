''' Genetic Algorithm example
a: kl & cl

A basic implementation of genetic algorithms (GA) in Python3. GA is a metaheuristic inspired by the process of evolution.
Shows the changes in genotypes (expressed by a sequence Boolean values in an array) over multiple generations,
matching the best-fitting genotype determined by an environment.

We will need to model the following GA principals
- intializing a population with its genetic representation
- creating a fitness function
- creating a selection function
- creating a goal/termination point

User configurable variables
peeps_n  -  population of our peep test subjects
top_n   -  arbritrary selection factor
        
                                   ___
                               ,-""   `.
                             ,'  _   e )`-._
                            /  ,' `-._<.===-'
                           /  /
                          /  ;
              _.--.__    /   ;
 (`._    _.-""       "--'    |
 <_  `-""                     \
  <`-                          :
   (__   <__.                  ;
     `-.   '-.__.      _.'    /
        \      `-.__,-'    _,'
         `._    ,    /__,-'
            ""._\__,'< <____
                 | |  `----.`.
                 | |        \ `.
                 ; |___      \-``
                 \   --<
                  `.`.<
                    `-'
                    hjw

        
'''
import random

        
# global vars   
goal_flag = False


# user configurable vars
peeps_n = 100
top_n = 10


# functions
def random_g(genotype_complexity=4):
  '''Returns a list with user-inputted boolean elements

  Keyword arguments:
  genotype_complexity -- int length of boolean (0,1) elements returned

  Example:
  >> random_g()
  >> [0,1,0,0]

  '''
  genotype = []
  for item in range(genotype_complexity):
    genotype.append(random.randint(0,1))
  return genotype

# unit test
#print(random_g())
#print(random_g(5))


def init_peeps(n=peeps_n,gc=4):
  '''Initializes and returns dictionary of peeps with key:value of id:genotype sequence

  Keyword arguments:
  n -- int length of dictionary returned (default: global peeps_n)
  gc   --   int length of boolean (0,1) elements returned, passes to function random_g (default: 4)

  Example:
  >> init_peeps()
  >> {0:[1,1,1,1], 2:[0,1,1,0], ...}

  '''
  # vars
  peeps = {}

  # populate peeps
  for peeps_id in range(n):
    peeps[peeps_id]=random_g(gc)

  return peeps

# unit test
# print(init_peeps())
# print(init_peeps(n=123,gc=10))


def init_goal(gc=4):
  '''Returns goal tuple with keyword argument gc as genotype complexity (int length of boolean (0,1) elements returned)'''
  return tuple(random_g(gc))

# unit test: should return a tuple with 4 elements
# print(init_goal())


def match_fitness(individual,goal):
  '''Subfunction for check_fitness(). Returns int sum(matching genes), matching being the same boolean element at the same index.

  Keyword arguments:
  individual  --  list of boolean elements (0,1) representing individual genotypes
  goal  --  tuple of boolean elements (0,1) representing ideal environmental genotype sequence

  Example:
  >> match_fitness([1,1,0,0],(1,0,0,1))
  >> 1

  '''
  # vars
  fitness_score = 0

  # iterate through [individual] and (goal)
  for index in range(len(individual)):
    if individual[index] == goal[index]:
      fitness_score+=1

  return fitness_score

#unit test, expects 1:
#print(match_fitness([0,0,1,1],(1,1,0,1)))


def check_fitness(peeps,goal):
  '''Evaluates fitness and returns dict of id:fitness_score.
  

  Keyword arguments:
  peeps   --  dict of individual peeps with corresponding genotype sequence ie. {1:[1,1,0,0], 2:[1,1,1,1],...}
  goal    --  tuple of ideal environment genotype sequence ie. (0,0,0,1)

  Example:
  >> check_fitness(peeps,goal)
  >> {0:3, 1:2, 2:0, 3:4,...}


  '''
  # vars
  peeps_fitness = {}

  for index in peeps.keys():
    fitness_score = match_fitness(peeps[index],goal)
    peeps_fitness[index] = fitness_score

  return peeps_fitness

# unit test
#test_peeps = {1:[1,1,1,1],2:[1,1,0,0],3:[0,0,0,1]}
#goal = (1,1,1,0)
#
#print(check_fitness(test_peeps,goal))


# checks if matches goal by comparing peeps_fitness list (list of integers from 0 to len(goal))
# returns True if match found else False
def check_solution(peeps_fitness,goal):
  '''Returns (True,id) if solution is found, else False.

  Keyword arguments:
  peeps_fitness -- dict id:score ie. {1:4,2:1,3:0,...}
  goal  --  tuple of ideal environment genotype sequence ie. (0,0,0,1)

  Example:
  >> check_solution(peeps_fitness,goal)
  >> (True, key)
  '''

  # vars
  goal_score = len(goal)
  
  # iterate through
  for index in peeps_fitness.keys():
    if peeps_fitness[index] == goal_score:
      return (True, index)

  return False

# unit test: should return True
# ut_peeps_fitness = {1:1,2:0,3:2}
# ut_goal = [0]
# print(check_solution(ut_peeps_fitness,ut_goal)) 


def selection(peeps_fitness,n=top_n):
  '''Returns dict of top fitness, id:score desc.

  Keyword arguments:
  peeps_fitness   --  dict of id:score
  n               --  int population limit
  
  '''
  pf_keys = sorted(peeps_fitness,key=peeps_fitness.get,reverse=True)
  pf_values = sorted(peeps_fitness.values(),reverse=True)

  return (pf_keys[:n],pf_values[:n])


# unit test
# pf = {1:1,2:5,3:1,4:10,5:9,6:4,7:0}
# n = 5
# print(selection(pf,n))


def illbeinmybunk(spf,peeps,peeps_n,p):
  '''Returns list of the next generation of peeps, based on selection survivors, populates up to peeps_n
  
  Assumes that there are only two genes: {0,1} with p(0)=1-p(1)

  Keyword arguments:
  spf                   --  tuple sorted_peeps_fitness desc list, (id,score)
  peeps                 --  dict original id:genotype
  peeps_n               --  int population for next generation
  p                     --  float 0...0.99 probability for recessive/dom of gene 1

  '''


  def gene_weighted(p):
    '''Assumes the two genes are 0 and 1, will returned weighted random choice'''
    genes = [0,1]
    gene_weight = [1-p,p]

    while True:
      resultant_gene = random.choices(genes,gene_weight,k=10)
      gene0 = resultant_gene.count(0)
      gene1 = resultant_gene.count(1)
      if gene0 != gene1:
        if gene1 > gene0:
          return 0
        else:
          return 1


  def breeding(peeps, p):
    '''Returns new individual's genotype from two randomly chosen survivors.'''
    parent1 = random.choice(list(peeps.keys()))
    parent2 = random.choice(list(peeps.keys()))

    # checks if it didnt pull the same parent twice
    while parent2 == parent1:
      parent2 = random.choice(list(peeps.keys()))

    # combines genes
    child = []

    for index in range(len(peeps[parent1])):
      gene1 = peeps[parent1][index]
      gene2 = peeps[parent2][index]
      if gene1 == gene2:
        child.append(gene1)
      else:
        child.append(gene_weighted(p))

    return child

  # unit test
  # peeps = {1:[1,1,0,1],2:[1,1,1,1],3:[0,0,1,0],4:[0,0,1,0]}
  # p = 0.6
  # print(breeding(peeps,p))


  # dict p_g (peeps_genotype) --> id:genotype
  p_g = {}

  # output children --> id:genotype
  children = {}

  # populate p_g (match spf to peeps)
  for index in spf[0]:
    p_g[index] = peeps[index]

  # populate resultant children with their new ids:genotypes
  for index in range(peeps_n):
    children[index] = breeding(p_g,0.6)

  return children


#main body of program
#program loops through phases until solution met or max loop counter met


# initialize population and goal
current_gen_peeps = init_peeps(n=peeps_n,gc=20)
goal = init_goal(20)
generation = 0

while not goal_flag:
  peeps_fitness = check_fitness(current_gen_peeps,goal)
  peep_check = check_solution(peeps_fitness,goal)
  if peep_check is not False:
    peep_id = peep_check[1]
    print('Peep ID: {}\nPeep Genotype: {}\nGoal Genotype: {}\nGeneration: {}'.format(peep_id,current_gen_peeps[peep_id],goal,generation))
    goal_flag = True
  else:
    # peeps get purged, I mean selected
    selected_peeps = selection(peeps_fitness)
    current_gen_peeps = illbeinmybunk(selected_peeps,current_gen_peeps,peeps_n,0.6)
    generation+=1

