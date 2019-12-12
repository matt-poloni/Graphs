from itertools import combinations
from math import ceil, sqrt
from random import choice, sample, randint
from collections import deque
from statistics import mean, median

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print(f"WARNING: Friendship already exists between {user_id} and {friend_id}")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        ids = set(range(1, numUsers+1))
        for i in ids:
            self.add_user(f"User {i}")
        # Create friendships
        numPairs = ceil((numUsers * avgFriendships) / 2)
        maxFriends = ceil(sqrt(numUsers - 1))
        while numPairs > 0:
            current = ids.pop()
            max = min(numPairs, maxFriends)
            friends = sample(ids, randint(1, max))
            for friend in friends:
                self.add_friendship(current, friend)
                numPairs -= 1

        

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        queue = deque()
        queue.append([user_id])
        while len(queue) > 0:
            path = queue.popleft()
            person = path[-1]
            friends = {p for p in self.friendships[person] if p is not user_id and p not in visited}
            for f in friends:
                visited[f] = [*path, f]
                queue.append(visited[f])
        return visited

    def user_network_coverage(self):
        percents = []
        degrees = []
        numUsers = len(self.users)
        for user in self.users:
            paths = self.get_all_social_paths(user)
            percents.append(len(paths) / (numUsers-1))
            for path in paths:
                degrees.append(len(paths[path]) - 1)
        return {
            "med_pct": mean(percents) * 100,
            "avg_deg": mean(degrees)
        }


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
    sg.populate_graph(1000, 5)
    print('COVERAGE:')
    coverage = sg.user_network_coverage()
    print(coverage)
