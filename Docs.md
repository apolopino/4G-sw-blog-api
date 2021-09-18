# API Usage

## Endpoints
- GET /people: returns all the people
- GET /people/:id : returns the details for a particular person
- GET /planets: returns all the planets
- GET /planets/:id : returns the details for a particular planet
- GET /users: returns the list of all registered users
- GET /users/favorites: return the list of favorites for a particular user declared in the body. Usage: In body, send `{ "user_id": int }`
- POST /favorite/planet/:planet_id : creates a new favorite for the given user with the planet id defined in the URL. In the body of the request include `{ "user_id": int }`
- POST /favorite/people/:people_id : creates a new favorite for the given user with the people id defined in the URL. In the body of the request include `{ "user_id": int }`
- DELETE /favorite/planet/:planet_id : deletes the favorite planet with given id for a particular user included in the body. In the body of the request include `{ "user_id": int }`
- DELETE /favorite/people/:people_id : deletes the favorite person with given id for a particular user included in the body. In the body of the request include `{ "user_id": int }`
