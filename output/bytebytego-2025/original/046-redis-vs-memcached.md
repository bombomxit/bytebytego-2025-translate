# 046 - Redis VS Memcached

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 97-97
- Figures: 1

## Figures

![Redis VS Memcached - figure 1](../assets/046/figure-01.png)

## Original Extracted Text

The diagram below illustrates the key differences.

The advantages of data structures make Redis a good choice for:

   ● Recording the number of clicks and comments for each post (hash)

   ● Sorting the commented user list and deduping the users (zset)

   ● Caching user behavior history and filtering malicious behaviors (zset, hash)

   ● Storing boolean information of extremely large data into small space. For example, login
      status, membership status. (bitmap)
