import multiprocessing
import pyaudio


class PlayBack():
    tamBuffer = 0
    formatoBits = 0
    canales = 0
    tasaMuestra = 0
    audio = pyaudio.PyAudio()
    flujo = None

    def __init__(self , tamBuffer=2048 , formatoBits=pyaudio.paInt16 , canales=1 , tasaMuestra=48000):
        self.tamBuffer = tamBuffer
        self.formatoBits = formatoBits
        self.canales = canales
        self.tasaMuestra = tasaMuestra
        self.flujo = self.audio.open(rate=tasaMuestra , format=formatoBits , input=True , output=True , channels=canales , frames_per_buffer=tamBuffer)


    def __play_back(self):
        """funcion que se encarga del I/O """
        while True:
            data = self.flujo.read(self.formatoBits , False)
            self.flujo.write(data)



    def run(self):
       proceso= multiprocessing.Process(target=self.__play_back())
       proceso.start()
       proceso.join()