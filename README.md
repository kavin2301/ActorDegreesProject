Hey there! 🎬 Welcome to the Actor Degrees Project!
Ever wondered how actors are connected through movies? Well, this project lets you find out just how many degrees of separation there are between any two actors. It’s like playing “Six Degrees of Kevin Bacon,” but you can pick any actors you want!
Here’s how it works: We’ve got some CSV files with all the data you need. The people.csv file lists actors with their IDs, names, and birth years. The movies.csv file has info on movies, including their IDs, titles, and release years. And stars.csv tells you which actors starred in which movies. Pretty cool, right?
We store all this info in some handy dictionaries. names help us look up actors by name, people map actor IDs to their details and movies, and movies map movie IDs to their details and actors.
The main part of the project is figuring out the shortest path between two actors. You just run the script and input two actor names, and it’ll show you how they’re connected through movies. The magic happens in the shortest_path function, which you must implement. This function finds the shortest path between two actors and returns a list of (movie_id, person_id) pairs that represent the connections.
To get started, clone the repo and run the script with the large dataset. If you hit any snags or have ideas for improvements, don’t hesitate to open an issue or submit a pull request. Enjoy exploring the movie world and discovering actor connections!
Feel free to use and modify this project as you like. Have fun!
