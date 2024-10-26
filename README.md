# otus-microservice-architecture-hw

## Основы работы с Kubernetes (Часть 2)

Чтобы запустить minkube c нуля выполняем команды:  
`make minikube:start`  
`make minikube:prepare`  
`make minikube:install`  

Если minikube уже готовый и нужно только применить манифесты:  
`make minikube:install`

Далее, чтобы получить ответ от сервиса:  
`make minikube:check`