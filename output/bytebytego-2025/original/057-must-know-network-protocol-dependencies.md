# 057 - Must-Know Network Protocol Dependencies

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 118-119
- Figures: 1

## Figures

![Must-Know Network Protocol Dependencies - figure 1](../assets/057/figure-01.png)

## Original Extracted Text

Understanding network protocol dependencies is essential for cybersecurity and networking. Here's
a quick understanding of the same:

   1. IPv4 and IPv6 are the foundation of all networking. ICMP and ICMPv6 handle diagnostics,
       while IPsec ensures secure communication.

   2. TCP and UDP support various protocols. SCTP and DCCP serve specific cases.

   3. Some TCP-based protocols are HTTP, SSH, BGP, RDP, IMAP, SMTP, POP, etc.

   4. UDP-based protocols are DNS, DHCP, SIP, RTP, NTP, etc.

   5. SSL/TLS encrypts HTTPS, IMAPS, and SMTPS.

   6. LDAP and LDAPs are used for directory services over TCP and secured with SSL/TLS.

   7. QUIC is a UDP-based replacement for TCP+TLS for faster, encrypted connections.

   8. MCP or Model Context Protocol is an emerging standard for communicating with LLMs.

Over to you: Which other network protocol will you add to the list?
