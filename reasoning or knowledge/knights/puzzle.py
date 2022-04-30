from sys import implementation
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# General knowledge
general_knowledge = And(

    Or(BKnave, BKnight),
    Not(And(BKnave, BKnight)),
    Or(CKnave, CKnight),
    Not(And(CKnave, CKnight))
)

# Puzzle 0
# A says "I am both a knight and a knave."
sentence0 = And(AKnight, AKnave)


knowledge0 = And(
    # Or(AKnave, AKnight),
    # Not(And(AKnave, AKnight)),
    # Implication(Not(AKnight), Not(sentence0)),
    # Implication(AKnight, sentence0)
    
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnight, sentence0)

)

# Puzzle 1
# A says "We are both knaves."
sentence0 = And(AKnave, BKnave)
# B says nothing.


knowledge1 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(AKnight, sentence0),
)

# Puzzle 2
# A says "We are the same kind."
sentence0 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
# B says "We are of different kinds."
sentence1 = Or(And(BKnight, AKnave), And(BKnave, AKnight))

knowledge2 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(AKnight, sentence0),
    Biconditional(BKnight, sentence1)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
sentence0 = Or(AKnave, AKnight)
# B says "A said 'I am a knave'."
# B says "C is a knave."
sentence1 = And(AKnave, CKnave)
# C says "A is a knight."
sentence2 = AKnight


knowledge3 = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),
    Biconditional(AKnight, sentence0),
    Biconditional(BKnight, sentence1),
    Biconditional(CKnight, sentence2)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
