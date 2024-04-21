# Camera Relax Monitoring

Данный скрипт использует вебкамеру для мониторинга активности пользователя и напоминает о необходимости делать
перерывы во время работы за компьютером. Если пользователь проводит за компьютером непрерывно 30 минут,
программа автоматически предложит сделать перерыв. Для сброса уведомления необходимо отойти от рабочего места
на 3 минуты. После этого можно будет продолжить работу. Также предусмотрена функция отложить перерыв на 5 минут.

```sh
pip install pipenv
pipenv install
pipenv run .\main.py
```

Если есть ошибка при запуске - скачайте конфиг

```
https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg
```

Положите его в `~\.cvlib\object_detection\yolo\yolov3\` (перезапишите имеющийся файл).


## Enable GPU

Все прекрасно работает и на CPU. Если всё устраивает, то можно использовать как есть.

Подготовка:
1) Установить VisualStudio 2022 с отмеченными пакетами для десктопной разработки C++ приложений
2) Установить CMake
3) Установить Nvidia CUDA toolkit cuda_**12.3.2**
4) Скачать cudnn-windows-x86_64-**8.9.7.29** тарбол и распаковать в `c:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3\`
5) Скачать NVidia Video_Codec_SDK_**12.1.14**.zip и распаковать в `c:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3\` (Interface->include; Lib->lib)
6) Установить Anaconda https://www.anaconda.com/download (со стандартным питоном у меня не взлетело)
7) Потом запускаем CMake и делаем всё, что рассказано в видосе https://www.youtube.com/watch?v=YsmhKar8oOc

Важно использовать совместимые версии cuda, cudnn и video-code-sdk. На более новых версиях у меня были ошибки при сборке.

Ссылки на руководства
https://www.youtube.com/watch?v=d8Jx6zO1yw0
https://www.youtube.com/watch?v=YsmhKar8oOc
https://www.jamesbowley.co.uk/qmd/opencv_cuda_python_windows.html

Таблица с версиями для указания в CUDA_ARCH_BIN
https://en.wikipedia.org/wiki/CUDA#GPUs_supported