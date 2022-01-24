import pyaudio
import wave
import os
import numpy as np
from tqdm import tqdm
defaultframes = 512

class textcolors:
    if not os.name == 'nt':
        blue = '\033[94m'
        green = '\033[92m'
        warning = '\033[93m'
        fail = '\033[91m'
        end = '\033[0m'
    else:
        blue = ''
        green = ''
        warning = ''
        fail = ''
        end = ''



def start_record(audioname):
    recorded_frames = []
    device_info = {}
    useloopback = False
    recordtime = 5
    
    #Use module
    p = pyaudio.PyAudio()

    #Set default to first in list or ask Windows
    try:
        default_device_index = p.get_default_output_device_info()['index']
    except IOError:
        default_device_index = -1
    
    input_info = input("use default speaker device for recording (Y or N):") or "Y"
    if input_info == "Y" or input_info == "y":
        use_default_device_flag = True
    else:
        use_default_device_flag = False
        
    if use_default_device_flag == False:
        #Select Device
        print (textcolors.blue + "Available devices:\n" + textcolors.end)
        for i in range(0, p.get_device_count()):
            info = p.get_device_info_by_index(i)
            print (textcolors.green + str(info["index"]) + textcolors.end + ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))

            if default_device_index == -1:
                default_device_index = info["index"]

        #Handle no devices available
        if default_device_index == -1:
            print (textcolors.fail + "No device available. Quitting." + textcolors.end)
            exit()


        #Get input or default
        device_id = int(input("Choose device [" + textcolors.blue + str(default_device_index) + textcolors.end + "]: ") or default_device_index)
        print ("")
    else:
        defualt_device_name = p.get_device_info_by_index(default_device_index)['name']
        for i in range(0, p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info["name"] == defualt_device_name and p.get_host_api_info_by_index(info["hostApi"])["name"] == 'Windows WASAPI':
                device_id = i;
                break
                
    #Get device info
    try:
        device_info = p.get_device_info_by_index(device_id)
    except IOError:
        device_info = p.get_device_info_by_index(default_device_index)
        print (textcolors.warning + "Selection not available, using default." + textcolors.end)

    #Choose between loopback or standard mode
    is_input = device_info["maxInputChannels"] > 0
    is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
    if is_input:
        print (textcolors.blue + "Selection is input using standard mode.\n" + textcolors.end)
    else:
        if is_wasapi:
            useloopback = True;
            print (textcolors.green + "Selection is output. Using loopback mode.\n" + textcolors.end)
        else:
            print (textcolors.fail + "Selection is input and does not support loopback mode. Quitting.\n" + textcolors.end)
            exit()

    
    #print(device_info["defaultSampleRate"])
    #Open stream
    channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
    stream = p.open(format = pyaudio.paInt16,
                    channels = channelcount,
                    rate = int(device_info["defaultSampleRate"]),
                    input = True,
                    frames_per_buffer = defaultframes,
                    input_device_index = device_info["index"],
                    as_loopback = useloopback)

    #Start Recording
    print (textcolors.blue + "Starting...\nPress q to end the recoding" + textcolors.end)
    import keyboard
    
    total = 10000
    pbar = tqdm(total)
    while True:
        recorded_frames.append(stream.read(defaultframes))
        pbar.update(1)
        if keyboard.is_pressed("q"):
            print("\nq pressed, end recoding")
            break
    pbar.close()
    '''   
    recordtime = int(input("Record time in seconds [" + textcolors.blue + str(recordtime) + textcolors.end + "]: ") or recordtime)    
    for i in trange(0, int(int(device_info["defaultSampleRate"]) / defaultframes * recordtime)):
        recorded_frames.append(stream.read(defaultframes))
        #print(".")
    
    print (textcolors.blue + "End." + textcolors.end)
    '''
    #Stop Recording

    stream.stop_stream()
    stream.close()

    #Close module
    p.terminate()

    #filename = input("Save as [" + textcolors.blue + "out.wav" + textcolors.end + "]: ") or "out.wav"
    filename = audioname

    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(channelcount)
    waveFile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(int(device_info["defaultSampleRate"]))
    waveFile.writeframes(b''.join(recorded_frames))
    waveFile.close()
    

    recorded_frames = np.array(recorded_frames)
    recorded_frames = np.frombuffer(recorded_frames,np.int16)
    recorded_frames = np.reshape(recorded_frames, (-1, 2))

    recorded_frames = recorded_frames[:,0]
    recorded_frames = recorded_frames[:,np.newaxis]
    
    origin_frames = recorded_frames
    recorded_frames = (recorded_frames - np.mean(recorded_frames)) / (np.std(recorded_frames) + 1e-15)
    return int(device_info["defaultSampleRate"]), recorded_frames, origin_frames

