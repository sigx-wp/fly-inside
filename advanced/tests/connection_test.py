from djitellopy import Tello

if __name__ == '__main__':
    print('1. Connection test:')
    tello = Tello()
    tello.connect()
    print('\n')

    print('Connection test passed.')

    print('2. Video stream test:')
    tello.streamon()
    print('\n')

    print('Video stream test passed.')

    tello.end()

    print('Test(s) passed, disconnected from Tello.')
