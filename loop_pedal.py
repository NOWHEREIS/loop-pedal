import pyaudio
from sense_hat import SenseHat
class LoopPedal:
    __tamanio_buffer = 2048
    __formato = pyaudio.paInt16
    __canales = 1
    __tasa_muestra = 48000
    __audio = pyaudio.PyAudio()
    __flujo=None
    __cuadros=[]

    def __init__(self, controlador_del_pedal=SenseHat(),entrada_de_audio=None,salida_de_audio=None):
        """ Este es el constructor del loop pedal"""
        self.controlador_del_pedal=controlador_del_pedal
        self.entrada_de_audio=entrada_de_audio
        self.salida_de_audio=salida_de_audio

        self.__flujo=self.__audio.open(rate=self.__tasa_muestra,channels=self.__canales,input=True,output=True,frames_per_buffer=self.__tamanio_buffer,
                                       format=self.__formato,input_device_index=entrada_de_audio,output_device_index=salida_de_audio)

    @staticmethod
    def get_devices():
        pa=pyaudio.PyAudio()
        for i in range(pa.get_device_count()):
            print(pa.get_device_info_by_index(i))

        pa.terminate()

    def record_until_button_pressed(self):
        while True:
            data= self.__flujo.read(self.__tamanio_buffer,False)
            self.__cuadros.append(data)
            eventList = self.controlador_del_pedal.stick.get_events()
            if eventList and (eventList[ 0 ].action == "pressed"):
                proceso.terminate()
                senseHat.clear()
                return

    def record_seconds(self,segundos_grabacion):
        for i in range(0,int(self.__tasa_muestra/self.__tamanio_buffer * segundos_grabacion)):
            data= self.__flujo.read(self.__tamanio_buffer,False)
            self.__cuadros.append(data)











