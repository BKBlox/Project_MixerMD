# Function to create random matches, avoiding self-matching
import random

def create_random_matches(users):
	shuffled_users = users[:]
	random.shuffle(shuffled_users)

	# Ensure no user is assigned to themselves
	for i in range(len(users)):
		while users[i] == shuffled_users[i]:
			for j in range(len(users)):
				random.shuffle(shuffled_users)  # Reshuffle if a user gets their own story

	matches = {users[i]: shuffled_users[i] for i in range(len(users))}
	return matches
