import csv 
from collections import deque 

#load data from csv files into the memory 
def load_data(directory):
    # Maps names to a set of corresponding person_ids
    names = {}
    
    # Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
    people = {}
    
    # Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
    movies = {}

    # Load people
    with open(f"{directory}/people.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            person_id = row["id"]
            people[person_id] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {person_id}
            else:
                names[row["name"].lower()].add(person_id)

    # Load movies
    with open(f"{directory}/movies.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie_id = row["id"]
            movies[movie_id] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            person_id = row["person_id"]
            movie_id = row["movie_id"]
            
            # Ensure the person_id exists in the people dictionary
            if person_id in people:
                people[person_id]["movies"].add(movie_id)
            else:
                print(f"Warning: person_id {person_id} not found in people.csv")

            # Ensure the movie_id exists in the movies dictionary
            if movie_id in movies:
                movies[movie_id]["stars"].add(person_id)

    return names, people, movies

#BFS 
def shortest_path(source, target, people, movies):
    #intitalize frontier with a source actor
    frontier = deque([(None, source)]) 
    explored = set()   
    parent = {}


    while frontier:
        #get the first node from the frontier 
        current_movie, current_person = frontier.popleft()

        #if current node is the target, reconstruct the path 
        if current_person == target:
            path = []
            while current_movie is not None:
                path.append((current_movie, current_person))
                current_movie, current_person = parent[(current_movie, current_person)]
            path.reverse()
            return path
        
        #Mark the current node as explored 
        explored.add(current_person)

        #add neighbours to the frontiers 
        for movie_id, person_id in neighbors_for_person(current_person, people, movies):
            if person_id not in explored and person_id not in [person for _, person in frontier]:
                frontier.append((movie_id, person_id))
                parent[(movie_id, person_id)] = (current_movie, current_person)

    #if reached here, no path was found unfortunately 
    return None

def neighbors_for_person(person_id, people, movies):
    if person_id not in people:
        print(f"Warning: Person ID {person_id} not found in people dataset.")
        return set()  # If person_id doesn't exist, return an empty set

    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        if movie_id in movies:
            for star_id in movies[movie_id]["stars"]:
                if star_id != person_id:  # Exclude the person themselves
                    neighbors.add((movie_id, star_id))
    return neighbors


def main():
    directory = "large"  # or "large" depending on the dataset size you want to use

    # Load data from files into memory
    print("Loading data...")
    names, people, movies = load_data(directory)
    print("Data loaded.")

    # Get names from the user
    source_name = input("Name: ")
    target_name = input("Name: ")

    source_id = person_id_for_name(source_name, names, people)
    if source_id is None:
        print(f"{source_name} not found.")
        return

    target_id = person_id_for_name(target_name, names, people)
    if target_id is None:
        print(f"{target_name} not found.")
        return

    # Find the shortest path
    path = shortest_path(source_id, target_id, people, movies)

    # Print results
    if path is None:
        print("No connection found.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        for i, (movie_id, person_id) in enumerate(path):
            movie = movies[movie_id]["title"]
            person = people[person_id]["name"]
            if i == 0:
                print(f"{i + 1}: {source_name} and {person} starred in {movie}")
            else:
                print(f"{i + 1}: {person} starred in {movie}")


def person_id_for_name(name, names, people):
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

if __name__ == "__main__":
    main()
