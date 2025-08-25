# Test Plan

## Unit Testing
The primary goal of unit testing is to validate the functionality of each component in isolation. This ensures that each individual part of the application behaves as expected before it is combined with others.

To achieve true isolation, unit tests will make extensive use of mocks and stubs. For example, when testing a function in the Service Layer, the Repository Layer it depends on will be mocked. This allows us to test the business logic of the service without any reliance on the actual data storage implementation.

## Integration Testing
Integration tests are designed to validate the connections and interactions between different layers of the application. While unit tests ensure each component works in isolation, integration tests ensure they work together correctly.

For this project, integration tests will use FastAPI's `TestClient`. This powerful utility allows us to make HTTP requests directly to the application's endpoints and inspect the full response, including status codes, headers, and JSON bodies. This approach effectively tests the entire application stack, from the API layer through the service and repository layers.

## In-Container Testing
A critical step in our quality assurance process is ensuring that the application behaves correctly in its production environment. To eliminate "it works on my machine" issues, all tests must be executed within the final, built Docker container.

The CI/CD pipeline will be configured to first build the production Docker image, and then run the entire `pytest` suite (both unit and integration tests) inside a container instantiated from that image. This guarantees that the tests are validating the exact same artifact that will be deployed, ensuring complete environment parity.

## API Edge Case and Validation Testing
To ensure the API is robust and handles bad input gracefully, we will systematically test for edge cases and validation failures. The primary tool for this will be `pytest.mark.parametrize`.

This feature allows us to define a single test function and run it multiple times with different inputs. We will use this to test the `POST /pokemon` endpoint with a variety of invalid payloads, such as:
- Missing `name` or `type` fields.
- Incorrect data types (e.g., `name` as a number).
- Empty strings for `name` or `type`.
- Submitting a Pokémon with a name that already exists.

For each parameterized case, the test will assert that the API returns the correct HTTP status code (e.g., 422 Unprocessable Entity, 409 Conflict) and a clear, descriptive error message in the response body.
