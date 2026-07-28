# 129 - Best Practices in API Design

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 270-271
- Figures: 1

## Figures

![Best Practices in API Design - figure 1](../assets/129/figure-01.png)

## Original Extracted Text

APIs are the backbone of communication over the Internet. Well-designed APIs behave consistently,
are predictable, and grow without friction. Some best practices to keep in mind are as follows:

   1. Use Clear Naming: When building an API, choose straightforward and logical names. Be
       consistent and stick with intuitive URLs that denote collections.

   2. Idempotency: APIs should be idempotent. They ensure safe retries by making repeated
       requests to produce the same result, especially for POST operations.

   3. Pagination: APIs should support pagination to prevent performance bottlenecks and payload
       bloat. Some common pagination strategies are offset-based and cursor-based.

   4. Sorting and Filtering: Query strings are an effective way to allow sorting and filtering of API
       responses. This makes it easy for developers to see what filters and sort orders are applied.

   5. Cross Resource References: Use clear linking between connected resources. Avoid
       excessively long query strings that make the API harder to understand.

   6. Rate Limiting: Rate limiting is used to control the number of requests a user can make to an
       API within a certain timeframe. This is crucial for maintaining the reliability and availability of
       the API.

   7. Versioning: When modifying API endpoints, proper versioning to support backward
       compatibility is important.

   8. Security: API security is mandatory for well-designed APIs. Use proper authentication and
       authorization with APIs using API Keys, JWTs, OAuth2, and other mechanisms.

Over to you: did we miss anything important?
