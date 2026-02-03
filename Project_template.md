## Изучите [README.md](README.md) файл и структуру проекта.

## Задание 1

[Целевая архитектура кинобездны](/schemas/diagrams/containers/cinemaabyss.svg)

## Задание 2

### 1. Proxy
[Реализация Proxy через nginx](src/microservices/proxy)

### 2. Kafka
[Реализация Events сервиса](src/microservices/events)


[Результат тестов](images/postman-tests.png) </br>
[Топики Kafka](images/kafka-topics.png)

## Задание 3

### CI/CD
[Обновленная сборка](.github/workflows/docker-build-push.yml)

### Proxy в Kubernetes
[Вызов https://cinemaabyss.example.com/api/movies](images/movies-call.png) </br>
[Логи event-service](images/event-service-logs.png)


## Задание 4
[Развертывание helm](images/helm-deployment.png) </br>
[Вывод https://cinemaabyss.example.com/api/movies](images/movies-call-2.png) </br>


# Задание 5
[Статистика circut breaker'a](images/fortio-circuit-breaker-test.png) </br>
