# 011 - How TikTok Manages a 200K File Frontend MonoRepo?

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 28-29
- Figures: 1

## Figures

![How TikTok Manages a 200K File Frontend MonoRepo? - figure 1](../assets/011/figure-01.png)

## Original Extracted Text

A MonoRepo, short for a monolithic repository, is a software development strategy where a single
repository contains multiple projects, libraries, and services.

The good parts of a MonoRepo are:

   ● Better code sharing

   ● Simplified dependency management

   ● A unified view of the code base

However, the bigger the MonoRepo gets, the slower the various Git operations.

TikTok faced a similar change with its frontend TypeScript MonoRepo with 200K files.

To deal with this, TikTok built a tool named Sparo that optimizes the performance of Git operations
for large frontend MonoRepos.

Sparo dramatically improved the performance of Git operations. Some stats are as follows

   ● Git clone time went from 40 mins to just 2 mins.

   ● Checkout went from 1.5 minutes to 30 seconds.

   ● Status went from 7 seconds to 1 second.

   ● Git commit time went from 15 seconds to 11 seconds.

Over to you: Have you used MonoRepos in your projects?
