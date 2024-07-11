# Mini Fastapi app
## Architecture Project

| MVC     | python                                                                                                      |
|---------|-------------------------------------------------------------------------------------------------------------|
| Model   | [app/dto/model](https://github.com/TheBaldFrog/miniCryptocurrencyTracker/tree/main/app/dto/model)           |
| View    | [app/dto/schema](https://github.com/TheBaldFrog/miniCryptocurrencyTracker/tree/main/app/dto/schema)         |
| Controller | [app/api/v1/routers](https://github.com/TheBaldFrog/miniCryptocurrencyTracker/tree/main/app/api/v1/routers) |
| Service | [app/service](https://github.com/TheBaldFrog/miniCryptocurrencyTracker/tree/main/app/service)               |

## [Repository](https://github.com/TheBaldFrog/miniCryptocurrencyTracker/tree/main/app/repository)
Intermediary layer between an [application’s business logic](https://github.com/TheBaldFrog/miniCryptocurrencyTracker/tree/main/app/service) and data storage.

### Backend
Enter the `miniCryptocurrencyTracker` directory

   ```shell
   docker-compose up -d
   ```
### Demo Backend
docs [Link](http://52.91.140.87/docs)

username -> `test` <br/>
password -> `test`

### Demo [Frontend](https://github.com/TheBaldFrog/miniCryptocurrencyTrackerFrontend)
[link](http://3.95.246.13/)
