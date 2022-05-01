# SE_14 AI Basics - Assessment Code Base
## Description

This repository has four folders, each corresponding to one area of AI (learning, optimization, reasoning and search). 
Each of those folders, holds one or two projects, in which methods of the related field of AI are used to solve a problem.

The assignments for the projects is taken from the course https://cs50.harvard.edu/ai/2020/. Each of the projects had an uncompleted code base. The task was to those, to make the projects run.

##  Overview of projects:
### Learning:
  - Nim
  
### Optimization:
  - Crossword
  
### Reasoning:
  - Knights and Knaves
  
### Search:
  - Degrees
  - TicTacToe
  
## Dependencies

Install requirements.txt with:

`pip3 install -r requirements.txt`


# Documentation of the projects

**Make sure you installed the dependencies**

## Nim

**How to run:**

1. Set x in  play.py (`ai = train(x)`) to the amount of games the AI should play befor facing you
2. Run the game with `python play.py` and follow the instruction in the terminal

**Functions which implementation needed to be completed:**

- get_q_value
- update_q_value
- best_future_reward
- choose_action

## Crossword

**How to run:**

Run `python generate.py data/structure0.txt data/words0.txt name_of_img.png`
- Change the crossword layout by changing `data/structure0.txt` to `data/structure1.txt` or `data/structure2.txt`
- Change the set of words by changing `data/words0.txt` to `data/words1.txt` or `data/words2.txt`
- The last argument `name_of_img.png` sets the name of the saved image, leave it blank to not save the image


**Functions which implementation needed to be completed:**
- enforce_node_consitency
- revise
- ac3
- assignment_complete
- consistent
- order_domain_values
- select_unassinged_variable
- backtrack

## Knights and Knaves

**How to run:**
Run `python puzzle.py`


**Functions which implementation needed to be completed:**

*No functions needed to be implemented for this project, only the sentences for each puzzle and the general information over the rules of the game*

## Degrees

**How to run:**

1. Run `python degrees.py` or `python degrees_optimized.py` (if you dont want to wait that long)
2. Copy and past each time a different name from large/people.csv, when the terminal asks for a name


**Functions which implementation needed to be completed:**

- shortest_path

## Tic-tac-toe

**How to run:**

1. Run `python runner.py`
2. Follow the instructions of the window which will open


**Functions which implementation needed to be completed:**

- player
- actions
- result
- winner
- terminal
- utility
- minimax




