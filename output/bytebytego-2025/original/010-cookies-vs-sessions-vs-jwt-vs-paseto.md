# 010 - Cookies Vs Sessions Vs JWT Vs PASETO

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 26-27
- Figures: 1

## Figures

![Cookies Vs Sessions Vs JWT Vs PASETO - figure 1](../assets/010/figure-01.png)

## Original Extracted Text

Authentication ensures that only authorized users gain access to an application's resources. It
answers the question of the user's identity i.e. "Who are you?"
The modern authentication landscape has multiple approaches: Cookies, Sessions, JWTs, and
PASETO. Here's what they mean:

   1. Cookies and Sessions
       Cookies and sessions are authentication mechanisms where session data is stored on the
       server and referenced via a client-side cookie.

       Sessions are ideal for applications requiring strict server-side control over user data. On the
       downside, sessions may face scalability challenges in distributed systems.

   2. JWT
       JSON Web Token (JWT) is a stateless, self-contained authentication method that stores all
       user data within the token.
       JWTs are highly scalable but require careful handling to mitigate the chances of token theft
       and manage token expiration.

   3. PASETO
       Platform-Agnostic Security Tokens or PASETO improve upon JWT by enforcing stronger
       cryptographic defaults and eliminating algorithmic vulnerabilities.
       PASETO simplifies token implementation by avoiding the risks associated with
       misconfiguration.

Over to you: Which authentication approach have you used?
