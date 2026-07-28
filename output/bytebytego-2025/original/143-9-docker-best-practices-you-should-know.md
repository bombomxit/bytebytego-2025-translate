# 143 - 9 Docker Best Practices You Should Know

- Source: ByteByteGo Big Archive System Design 2025
- PDF pages: 295-296
- Figures: 1

## Figures

![9 Docker Best Practices You Should Know - figure 1](../assets/143/figure-01.png)

## Original Extracted Text

1. Use official images
     This ensures security, reliability, and regular updates.

 2. Use a specific image version
     The default latest tag is unpredictable and causes unexpected behavior.

 3. Multi-Stage builds
     Reduces final image size by excluding build tools and dependencies.

   4. Use .dockerignore
       Excludes unnecessary files, speeds up builds, and reduces image size.

   5. Use the least privileged user
       Enhances security by limiting container privileges.

   6. Use environment variables
       Increases flexibility and portability across different environments.

   7. Order matters for caching
       Order your steps from least to most frequently changing to optimize caching.

   8. Label your images
       It improves organization and helps with image management.

   9. Scan images
       Find security vulnerabilities before they become bigger problems.

Over to you: Which other Docker best practices will you add to the list?
