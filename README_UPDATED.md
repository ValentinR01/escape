
# Technical Test

A brief description of this test 

## Init 
I struggled with Prisma container openssl dependence issue. I tried to reinstall the package installed on the Dockerfile and tried to specify other openssl version on schema. Prisma but without success. I Finally thought it might be related to a new alpine release, so I rollbac


### 1.1 - Create a task model
Took some time to refresh on Prisma, but was OK :) 

### 1.2 - Create a task
I followed the project structure and created new libs and routes files.

### 1.3 - List the tasks of the authenticated user
Was easy because the auth Middleware was already implemented 

### 1.4 - Publish a message on the broker when a task is created
Was easy because the Kafka Service was already created 

## Exercice 2: Have the tasks service handling tasks

### 2.1 - Listen on the `task.created` topic
I tried to find a way to run concurrently both consumer's runner. Spent way too much time on it for no result. I ended up switching from one asyncio consumer to another.

### 2.2 - Publish a message on the broker when a task's status changes
As for the Node.js part, the Kafka Class and producer method was already implemented, it wasn't too difficult. 

### 2.3: Make sure many tasks can be handled simultaneously
No time left :/ 


## Overall 
I thought this test was more about the underlying Kafka Infrastructure / Dockerization / Infra than development. I tried to be ready for it with Kafka compose stack, Avro Schemas, Kafka security etc
