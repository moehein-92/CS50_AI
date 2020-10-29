from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
sentence = And(AKnight, AKnave)
knowledge0 = And(
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),

    Implication(AKnight, sentence),
    Implication(AKnave, Not(sentence))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentenceA1 = And(AKnave, BKnave)
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Biconditional(AKnight, sentenceA1)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentenceA2 = Or(And(AKnight, AKnave), And(AKnave, BKnave))
sentenceB2 = Or(And(AKnight, AKnave), And(AKnave, BKnight))

knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Biconditional(AKnight, sentenceA2),
    Biconditional(BKnight, sentenceB2)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
sentenceA3 = Biconditional(AKnight, Not(AKnave))
sentenceB3 = And(Biconditional(AKnight, BKnave), CKnave)
sentenceC3 = AKnight

knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    Biconditional(AKnight, sentenceA3),
    Biconditional(BKnight, sentenceB3),
    Biconditional(CKnight, sentenceC3)
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
