import bcrypt
import time

for rounds in [6, 8, 10, 12]:
    start_time = time.time()
    bcrypt.gensalt(rounds=rounds)
    print(f"Rounds: {rounds}, Time taken: {time.time() - start_time} seconds")