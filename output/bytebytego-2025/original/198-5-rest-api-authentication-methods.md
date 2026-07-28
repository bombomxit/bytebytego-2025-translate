# 198 - 5 REST API Authentication Methods

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 403-404
- Figures: 1

## Figures

![5 REST API Authentication Methods - figure 1](../assets/198/figure-01.png)

## Original Extracted Text

1. Basic Authentication: Clients include a Base64-encoded username and password in every
     request header, which is simple but insecure since credentials are transmitted in plaintext.
     Useful in quick prototypes or internal services over secure networks.

 2. Session Authentication: After login, the server creates a session record and issues a cookie.
     Subsequent requests send that cookie so the server can validate user state. Used in
     traditional web-apps.

 3. Token Authentication: Clients authenticate once to receive a signed token, then present the
     token on each request for stateless authentication. Used in single-page applications and
     modern APIs that require scalable, stateless authentication.

4. OAuth-Based Authentication: Clients obtain an access token via an authorization grant from
    an OAuth provider, then use that token to call resource servers on the user's behalf. Used in
    cases of third-party integrations or apps that need delegated access to user data.

5. API Key Authentication: Clients present a predefined key (often in headers or query strings)
    with each request. The server verifies the key to authorize access. Used in service-to-service
    or machine-to-machine APIs where simple credential checks are sufficient.
