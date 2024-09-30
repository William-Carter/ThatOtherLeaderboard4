import random
def getVerificationWord(id: int) -> str:
        random.seed(id)
        num = random.randint(0, 999)
        with open("deletion/verificationWords.txt", "r") as f: 
            word = (f.readlines()[num]).rstrip()

        return word