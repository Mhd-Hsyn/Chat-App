# Project README

This repository contains a Django project for a simple chat application with user authentication using JWT tokens. Below, we'll explain the project flow, API endpoints, and how scalability and security are handled.

## Encryption and Decryption for User Messages

User messages are encrypted before being stored in the database to ensure data security. This encryption is implemented using the Fernet symmetric encryption algorithm provided by the `cryptography` library. Each message is encrypted with a unique key, ensuring data confidentiality.

During message retrieval, the encrypted messages are decrypted on-the-fly before being returned to the user. This ensures that users can view their messages in plaintext format while maintaining data security during storage.

The encryption and decryption process adds an additional layer of security to the chat application, ensuring that user communication remains private and secure.


## Project Flow

1. **User Authentication**: Users can sign up with a unique email and password. Passwords are hashed using PBKDF2 and validated. Upon successful signup, users receive JWT tokens, which are used for subsequent authentication.

2. **User Login**: Existing users can log in using their email and password. Upon successful login, users receive JWT tokens.

3. **Chat Creation**: Authenticated users can create chat rooms.

4. **Messaging**: Authenticated users can send messages within created chat rooms.

## API Endpoints

### User Authentication

- `POST /userauth/userSignup`: Endpoint for user signup. Requires a unique email and a password with a length of at least 8 characters. Returns a success message upon successful signup.
  - Body: `{ "email": "user@example.com", "password": "password123", "fname": "John", "lname": "Doe", "profile": "profile_image.jpg" }`
  - Authentication: Not required.

- `POST /userauth/userLogin`: Endpoint for user login. Requires a registered email and matching password. Returns a JWT token upon successful login.
  - Body: `{ "email": "user@example.com", "password": "password123" }`
  - Authentication: Not required.

### Chat Operations

- `POST /chat/`: Endpoint for creating a new chat room. Requires authentication.
  - Body: `{ "chat_name": "New Chat" }`
  - Authentication: Bearer token required.

- `GET /chat/`: Endpoint for retrieving all chat rooms. Requires authentication.
  - Authentication: Bearer token required.

### Messaging

- `POST /message/`: Endpoint for sending a message in a chat room. Requires authentication.
  - Body: `{ "chatid": "chat_id_here", "message": "Hello, world!" }`
  - Authentication: Bearer token required.

- `GET /message/`: Endpoint for retrieving messages in a specific chat room. Requires authentication.
  - Query Parameters: `chat_id` (ID of the chat room)
  - Authentication: Bearer token required.

## Scalability and Security

## Encryption and Decryption for User Messages

User messages are encrypted before storing them in the database and decrypted before being retrieved. This ensures that messages are secure and can only be viewed by authorized users.

### Scalability

- **Token-based Authentication**: JWT tokens are used for authentication, reducing the need for frequent database queries during user sessions, enhancing scalability.
  
### Security

- **Password Hashing**: User passwords are hashed using PBKDF2, ensuring that plaintext passwords are never stored.
  
- **JWT Tokens**: JWT tokens are used for authentication, providing a secure and stateless method for user verification.
  
- **Permission Control**: Custom permission classes are implemented to control access to API endpoints based on user authentication.

- **Input Validation**: Input data is validated using serializers to ensure that only valid data is processed, mitigating potential security vulnerabilities.

- **Error Handling**: Exception handling is implemented to handle errors gracefully and provide informative responses without exposing sensitive information.

- **Token Whitelisting**: JWT tokens are stored in a whitelist upon user login to ensure that only valid tokens are accepted for subsequent requests, enhancing security.

---

