from play_back import PlayBack
import loop_pedal

if __name__ == '__main__':
    loop_pedal.LoopPedal.get_devices()

    p=PlayBack()
    p.run()



