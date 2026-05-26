# Отчет по лабораторной работе: Docker и контейнеризация IoT-системы

## Архитектура системы

Система построена на базе трёх виртуальных машин из Лабораторной работы 1 и реализует IoT-мониторинг с помощью Docker-контейнеров.

```
[Linux A / smirnovclient 192.168.10.10]
  └── 6 симуляторов датчиков (Docker)
        └── публикует данные по MQTT →

[Linux B / smirnovgateway 192.168.10.1]
  └── Mosquitto MQTT брокер (Docker, порт 1883)
        └── передаёт данные →

[Linux C / smirnovserver 192.168.15.10]
  └── Telegraf → InfluxDB 1.8 → Grafana (docker-compose, порт 3000)
```

---

## 1. Linux B (smirnovgateway) — MQTT брокер

### Установка Docker и запуск Mosquitto

```bash
sudo apt install -y docker.io
sudo ufw allow 1883/tcp
sudo docker run -d --name broker -p 1883:1883 eclipse-mosquitto
```

### mosquitto.conf

```
listener 1883
allow_anonymous true
```

---

## 2. Linux A (smirnovclient) — Симуляторы датчиков

### Установка Docker

```bash
sudo apt install -y docker.io docker-compose
```

### Классы датчиков

Реализован базовый класс `Sensor` и 4 наследника с формулами на основе даты рождения (15.10.2002):

| Тип | Класс | Диапазон | Формула |
|-----|-------|----------|---------|
| Температура | `Temperature` | ~15–35 °C | амплитуда = BIRTH_DAY / 3 = **5** |
| Давление | `Pressure` | ~740–780 мм рт.ст. | смещение = BIRTH_MONTH / 10 = **1.0** |
| Ток | `Current` | 0–5 А | масштаб = (BIRTH_YEAR % 100) * 0.005 = **10.01** |
| Влажность | `Humidity` | 30–90 % | шаг = BIRTH_DAY / 15 = **1.0** |

### Переменные среды

| Переменная | Описание | Пример |
|------------|----------|--------|
| `SIM_HOST` | IP брокера | `192.168.10.1` |
| `SIM_NAME` | Имя датчика | `temp_room1` |
| `SIM_PERIOD` | Интервал (сек) | `5` |
| `SIM_TYPE` | Тип датчика | `temperature` |
| `SIM_TOPIC_FORMAT` | Формат: `plain` или `json` | `plain` |

### Сборка и публикация образа

```bash
cd ~/simulator
sudo docker build -t mikesma1/data-simulator .
sudo docker login -u mikesma1
sudo docker push mikesma1/data-simulator
```

Образ: `docker.io/mikesma1/data-simulator`

### Запуск 6 контейнеров

```bash
sudo docker-compose up -d
```

Запущено 6 контейнеров: temp_sensor_1, temp_sensor_2, pressure_sensor_1, pressure_sensor_2, current_sensor_1, humidity_sensor_1.

---

## 3. Linux C (smirnovserver) — Стек мониторинга

### Установка и запуск

```bash
sudo apt install -y docker.io docker-compose
cd ~/infra
sudo docker-compose up -d
```

Запущены контейнеры в сети `server-net`:
- `influxdb` — база данных (порт 8086)
- `telegraf` — подписка на MQTT топики `sensors/#`, запись в InfluxDB
- `grafana` — дашборды (порт 3000)

Все контейнеры взаимодействуют по alias (не по IP).

### Результат — Grafana Dashboard

Открыть: `http://192.168.15.10:3000` (admin/admin)

Дашборд **IoT Sensors Dashboard** отображает текущие значения всех датчиков в реальном времени (обновление каждые 5 секунд):

| Датчик | Значение |
|--------|----------|
| current_line_A | ~0.06 А |
| humidity_main | ~57 % |
| pressure_backup | ~760 мм рт.ст. |
| pressure_main | ~753 мм рт.ст. |
| temp_room1 | ~30 °C |
| temp_room2 | ~26 °C |

---

## 4. Инструкция по запуску

### Linux B — брокер
```bash
cd vms/gateway/mosquitto
bash run_broker.sh
```

### Linux A — симуляторы
```bash
cd vms/client/simulator
sudo docker-compose up -d
```

### Linux C — мониторинг
```bash
cd vms/server/infra
sudo docker-compose up -d
```

---

## 5. Структура репозитория

```
root/
├── assets/images/
├── vms/
│   ├── client/simulator/
│   │   ├── entity/__init__.py
│   │   ├── entity/sensor.py
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── requirements.txt
│   ├── gateway/mosquitto/
│   │   ├── mosquitto.conf
│   │   └── run_broker.sh
│   └── server/infra/
│       ├── docker-compose.yml
│       ├── grafana/provisioning/
│       │   ├── dashboards/default.yaml
│       │   ├── dashboards/mqtt.json
│       │   └── datasources/default.yaml
│       ├── influxdb/scripts/influxdb-init.iql
│       └── telegraf/telegraf.conf
└── report.md
```

## 6. Docker Hub

```bash
docker pull mikesma1/data-simulator
```
