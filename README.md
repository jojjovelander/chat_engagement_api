# Student Engagement Chatbot API

This API provides endpoints for managing student engagement chatbot data using FastAPI.

## Models

The API provides access to the following models:

- **User**: Represents a user in the system
- **Role**: Represents a user role
- **Group**: Represents a group of users
- **Thread**: Represents a conversation thread
- **Message**: Represents a message in a thread
- **Image**: Represents an image attached to a thread
- **UserGroup**: Represents a user's membership in a group

## API Endpoints

### Role Endpoints

- `POST /roles/`: Create a new role
- `GET /roles/`: Get all roles
- `GET /roles/{role_id}`: Get a specific role by ID

### User Endpoints

- `POST /users/`: Create a new user
- `GET /users/`: Get all users
- `GET /users/{user_id}`: Get a specific user by ID
- `GET /users/{user_id}/with-role`: Get a user with its associated role
- `GET /users/{user_id}/with-relations`: Get a user with all its related data (role, threads, user groups)

### Group Endpoints

- `POST /groups/`: Create a new group
- `GET /groups/`: Get all groups
- `GET /groups/{group_id}`: Get a specific group by ID
- `GET /groups/{group_id}/with-relations`: Get a group with all its related data (threads, user groups)

### Thread Endpoints

- `POST /threads/`: Create a new thread
- `GET /threads/`: Get all threads
- `GET /threads/{thread_id}`: Get a specific thread by ID
- `GET /threads/{thread_id}/with-relations`: Get a thread with all its related data (user, group, messages, images)

### Message Endpoints

- `POST /messages/`: Create a new message
- `GET /messages/`: Get all messages
- `GET /messages/{message_id}`: Get a specific message by ID

### Image Endpoints

- `POST /images/`: Create a new image
- `GET /images/`: Get all images
- `GET /images/{image_id}`: Get a specific image by ID

### UserGroup Endpoints

- `POST /user-groups/`: Create a new user group association
- `GET /user-groups/`: Get all user group associations
- `GET /user-groups/{user_group_id}`: Get a specific user group association by ID

## Fetching Models with Associated Submodels

The API provides special endpoints to fetch models with their associated submodels:

### User with Role

```
GET /users/{user_id}/with-role
```

Returns a user with its associated role.

### User with All Relations

```
GET /users/{user_id}/with-relations
```

Returns a user with all its related data:
- Role
- Threads
- User Groups

### Group with All Relations

```
GET /groups/{group_id}/with-relations
```

Returns a group with all its related data:
- Threads
- User Groups

### Thread with All Relations

```
GET /threads/{thread_id}/with-relations
```

Returns a thread with all its related data:
- User
- Group
- Messages
- Images

## Running the API

To run the API:

```bash
python main.py
```

This will start the server at http://0.0.0.0:8000.

You can access the interactive API documentation at http://0.0.0.0:8000/docs.