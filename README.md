# resuelve.leonardo
ResuelveTuDeuda Interview

## Prerequisites
Install docker on your computer
https://docs.docker.com/install/

## How to execute it

```
docker-compose up
```

### Try it
```
curl 127.0.0.1:5000/calcula_sueldo -v -H "Content-Type: application/json" -d '[{"nombre":"leonidas", "sueldo": 45000.0, "bono": 10000, "equipo":"xyz", "nivel":"A", "sueldo_completo":null, "goles":3}]'
```

## Running the tests

```
docker-compose run test
```
