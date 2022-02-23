# Page loader project
### Github actions with inner and linter tests and Hexlet tests:
[![Actions Status](https://github.com/dutlov/python-project-lvl3/actions/workflows/pyci.yml/badge.svg)](https://github.com/dutlov/python-project-lvl3/actions)
[![Actions Status](https://github.com/dutlov/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/dutlov/python-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/1114cc5dd8eea46effbc/maintainability)](https://codeclimate.com/github/dutlov/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/1114cc5dd8eea46effbc/test_coverage)](https://codeclimate.com/github/dutlov/python-project-lvl3/test_coverage)
______

### Описание:
page-loader - утилита, которая скачивает страницу из сети и сохраняет ее в указанную директорию (по умолчанию в директорию запуска программы) для дальнейшего использования оффлайн.
______

### Установка:
`pip install git+https://github.com/dutlov/python-project-lvl3.git`

### Использование:
`$ page-loader --output=/var/tmp https://hexlet.io/courses`  
Где:  
`$ page-loader` - вызов утилиты  
`--output` + `=/path` - указываем путь до дириектории(по умолчания сохраняет в директорию вызова)  
`https://hexlet.io/courses` - любая рабочая URL ссылка  
`page-loader -h` - помощь  

__________

### Демонстрация работы утилиты:
[![asciicast](https://asciinema.org/a/OsOqSA782cHXspQaE0JeV3Dz3.svg)](https://asciinema.org/a/OsOqSA782cHXspQaE0JeV3Dz3)
