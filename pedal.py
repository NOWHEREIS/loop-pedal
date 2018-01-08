import pyaudio
import wave
from sense_hat import SenseHat as sh
from multiprocessing import Process


##funciones
def mostrarMensaje(mensaje):
    senseHat.show_message(mensaje, 0.03 , [ 255 , 0 , 0 ])


senseHat = sh()  # llamada a sense hat


CHUNK = 2048  # tamaño del buffer
FORMAT = pyaudio.paInt16 #formato audio en bits
CHANNELS = 1 # canales
RATE = 48000 # muestras
WAVE_OUTPUT_FILENAME = "output.wav" #nombre del archivo salida

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT ,
                channels=CHANNELS ,
                rate=RATE ,
                input=True ,
                frames_per_buffer=CHUNK)

# print("* recording")


frames = []

if senseHat.stick.wait_for_event().action == "pressed":
    proceso = Process(target= mostrarMensaje,args=("grabando...",))
    proceso.start()
    #threading.Thread(target=mostrarMensaje , args=("grabando..." ,)).run()
    # senseHat.show_message("grabando", 0.05, [255, 0, 0])
    while True:
        data = stream.read(CHUNK , False)
        frames.append(data)
        eventList = senseHat.stick.get_events()
        if eventList and (eventList[0].action == "pressed"):
            proceso.terminate()
            senseHat.clear()
            break


    proceso.join()


proceso = Process(target=mostrarMensaje,args=("grabacion finalizada",))
proceso.start()

stream.stop_stream()
stream.close()

wf = wave.open(WAVE_OUTPUT_FILENAME , 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))

wfout = wave.open("output.wav", 'rb')
stream_out=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,output=True)
proceso.join()
eventList= senseHat.stick.wait_for_event(True).action
if (eventList == 'pressed'):
    proceso = Process(target=mostrarMensaje , args=("reproduciendo..." ,))
    proceso.start()
    data = wfout.readframes(CHUNK)
    while True :
        stream_out.write(data)
        data = wfout.readframes(CHUNK)
        if data=='':
            wfout.rewind()
            data=wfout.readframes(CHUNK)
            #sleep(0.5)

        eventList=senseHat.stick.get_events()

        if eventList and (eventList[0].action == "pressed"):
            break

proceso.join()




stream_out.stop_stream()
stream_out.close()
p.terminate()
mostrarMensaje("terminado")

