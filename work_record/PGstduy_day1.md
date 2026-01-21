# Architecture
- based on process
- When Postgre get connection require, it copys itself by fork() to generate process that mapping with client by 1:1
- It is expensive because it generates proecess for every request


# Memory management
Memory can be seprated two parts. One is Shared part, the other one is isolated part

-Shared buffers
  - 
