# guidance-platform
a platform where users can exchange experience regarding any given topic with people who have relevant knowledge and experience.
Guidance combines reciprocal user matching with AI-powered semantic recommendations to help users discover potential helpers, exchange knowledge, and learn from one another.

## Features

### User Profiles and Topic Management
- User registration and authentication.
- Personal profiles with editable biographies.
- Users can specify topics they can guide others on.
- Users can specify topics on which they need guidance.
- Experience levels: Beginner, Intermediate, and Advanced in the topics which they can guide other users on.

### Reciprocal User Matching
- Matches users based on complementary knowledge and learning interests.
- Identifies situations where two users can guide each other.
- Displays the topics on which each user can provide guidance.

### Guidance Requests
- Users can create guidance requests with titles, descriptions, and associated topics, in other words asking for guidance in a specific topic of their choice.
- Browse other users' open requests.
- View individual request details.
- Track personal guidance requests and their statuses.

### Guidance Offers
- Users can offer help to other people's guidance requests when stumbling upon a guidance request in a topic which they have relevant experience in.
- Request owners can accept or decline those offers which are sent to a targeted request to guide.
- Accepted offers move the associated request into the In Progress status.
- Competing pending offers are automatically declined when an offer is accepted.

### AI-Powered Semantic Recommendations
- Integrates the FastEmbed library and the `BAAI/bge-small-en-v1.5` embedding model.
- Converts guidance requests and potential helpers' topic descriptions into numerical embeddings.
- Uses cosine similarity to identify semantically related content.
- Ranks potential helpers according to their similarity scores.
- Supports recommendations based on related concepts, even when their wording differs.

For example, a user requesting help with Docker may receive recommendations from someone whose expertise is described as containerization, even when the topic names are not identical.

The recommendation system uses an embedding model rather than a generative LLM. It does not generate answers or explanations; it measures semantic similarity between text.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Django | Backend web framework |
| PostgreSQL | Relational database |
| Docker | Application containerization |
| Docker Compose | Management of application and database services |
| FastEmbed | Text embedding generation |
| BAAI/bge-small-en-v1.5 | Semantic embedding model |
| NumPy | Cosine similarity calculations |
| HTML | Frontend templates |

## AI Recommendation Workflow

The semantic recommendation process follows these steps:

1. Retrieve the user's open guidance requests.
2. Combine each request's title and description into a text input.
3. Retrieve other users who have registered topics they can guide others on.
4. Combine each helper's topic name and description into text inputs.
5. Generate embeddings using FastEmbed.
6. Calculate cosine similarity between the request embedding and each helper-topic embedding.
7. Keep the highest-scoring topic for each potential helper.
8. Sort potential helpers by similarity score in descending order.
9. Display the recommendations in the Django application.


## Database Models

The application uses Django ORM with PostgreSQL.

Its main models include:

- **Topic:** Stores topics and their descriptions.
- **UserTopic:** Associates users with topics and identifies whether they can guide others or need guidance.
- **Profile:** Stores additional user profile information.
- **GuidanceRequest:** Stores guidance requests and their statuses.
- **GuidanceOffer:** Stores offers submitted by potential helpers.

Database relationships and constraints help maintain data integrity and prevent duplicate topic relationships and duplicate offers for the same request.


## Author

**Mayas Rizq**

Backend Development | Django | Python

GitHub: [Mayas-dev](https://github.com/Mayas-dev)
