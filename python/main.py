import sound_record 
from sound_record import textcolors
from sound_classification import AudioSource
from argparse import ArgumentParser, SUPPRESS
import logging
import sys
import time
import wave
from scipy.io.wavfile import write
import numpy as np
import subprocess as sp
from openvino.inference_engine import IECore


def type_overlap(arg):
    if arg.endswith('%'):
        res = float(arg[:-1]) / 100
    else:
        res = int(arg)
    return res
    
    
def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')

    args.add_argument('--input', type=str, required=True,
                      help="Required. input file of video or audio")
    args.add_argument('--audioname', type=str, required=True,
                      help="Required. audio name for the recorded file")
    args.add_argument('-m', "--model", type=str, required=True,
                      help="Required. Path to an .xml file with a trained model.")
    args.add_argument("-l", "--cpu_extension", type=str, default=None,
                      help="Optional. Required for CPU custom layers. Absolute path to a shared library with "
                           "the kernels implementations.")
    args.add_argument("-d", "--device", type=str, default="CPU",
                      help="Optional. Specify the target device to infer on; CPU, GPU, HDDL or MYRIAD is"
                           " acceptable. The demo will look for a suitable plugin for device specified. "
                           "Default value is CPU")
    args.add_argument('--labels', type=str, default="aclnet_53cl.txt",
                      help="Optional. Labels mapping file")
    args.add_argument('--soundtype', type=str, default="Gunshot",
                      help="Optional. sound intended to extract")
    args.add_argument('-sr', '--sample_rate', type=int,
                      help="Optional. Set sample rate for audio input")
    args.add_argument('-ol', '--overlap', type=type_overlap, default=0,
                      help='Optional. Set the overlapping between audio clip in samples or percent')

    return parser.parse_args()

def main():
    args = build_argparser()

    logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO, stream=sys.stdout)
    log = logging.getLogger()
        
    #sound_record.start_record()
    
    log.info("Creating Inference Engine")
    ie = IECore()

    if args.device == "CPU" and args.cpu_extension:
        ie.add_extension(args.cpu_extension, 'CPU')

    log.info("Loading model {}".format(args.model))
    net = ie.read_network(args.model, args.model[:-4] + ".bin")

    if len(net.input_info) != 1:
        log.error("Demo supports only models with 1 input layer")
        sys.exit(1)
    input_blob = next(iter(net.input_info))
    input_shape = net.input_info[input_blob].input_data.shape
    if len(net.outputs) != 1:
        log.error("Demo supports only models with 1 output layer")
        sys.exit(1)
    output_blob = next(iter(net.outputs))

    log.info("Loading model to the plugin")
    exec_net = ie.load_network(network=net, device_name=args.device)

    log.info("Preparing input")

    labels = []
    if args.labels:
        with open(args.labels, "r") as file:
            labels = [line.rstrip() for line in file.readlines()]

    batch_size, channels, one, length = input_shape
    #[1, 1, 1, 16000]
    if one != 1:
        raise RuntimeError("Wrong third dimension size of model input shape - {} (expected 1)".format(one))

    audio = AudioSource(args.audioname, channels=channels, samplerate=args.sample_rate)

    hop = length - args.overlap if isinstance(args.overlap, int) else int(length * (1.0 - args.overlap))
    #hop = 16000
    if hop < 0:
        log.error("Wrong value for '-ol/--overlap' argument - overlapping more than clip length")
        sys.exit(1)

    log.info("Starting inference")
    outputs = []
    clips = 0
    infer_time = 0
    
    detect_flag = False
    time_count = 0
    save_duration = 5
    for idx, chunk in enumerate(audio.chunks(length, hop, num_chunks=batch_size)):
        #1,1,16000 one chunk
        if time_count > save_duration / (length / audio.samplerate):
            detect_flag = False
            time_count = 0
        if detect_flag:
            time_count +=1
            continue
        chunk.shape = input_shape
        infer_start_time = time.perf_counter()
        output = exec_net.infer(inputs={input_blob: chunk})
        infer_time += time.perf_counter() - infer_start_time
        clips += batch_size
        output = output[output_blob]
        for batch, data in enumerate(output):
            #audio.samplerate = 48000
            start_time = (idx*batch_size + batch)*hop / audio.samplerate
            end_time = ((idx*batch_size + batch)*hop + length) / audio.samplerate
            outputs.append(data)
            label = np.argmax(data)
            if labels[label] == args.soundtype:
                detect_flag = True
                detected_chunk = audio.origin_data[(idx*batch_size + batch)*hop: (idx*batch_size + batch)*hop + audio.samplerate*save_duration,:]
                write(str(np.ceil(start_time))+'.wav', audio.samplerate, detected_chunk)
                
                #save video clip
                if "mp4" in args.input:
                    sp.call('ffmpeg.exe -ss {} -i "{}" -t {} -c copy {} -loglevel quiet'.format(np.ceil(start_time), args.input, save_duration, str(int(np.ceil(start_time)))+'.mp4'), shell=True)

            if start_time < audio.duration():
                if detect_flag == True:
                    log.info("[{:.2f}-{:.2f}] - {:6.2%} {:s} {}File is saved.{}".format(start_time, end_time, data[label],
                                                              labels[label] if labels else "Class {}".format(label) ,textcolors.green, textcolors.end))
                else:
                    log.info("[{:.2f}-{:.2f}] - {:6.2%} {:s}".format(start_time, end_time, data[label],
                                                              labels[label] if labels else "Class {}".format(label)))
            if detect_flag == True:
                break
    #logging.info("Average infer time - {:.1f} ms per clip".format(infer_time / clips * 1000))


if __name__ == '__main__':
    main()
    
    
# after recording, the accuracy is lower than before. 会有误判