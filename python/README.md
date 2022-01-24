* Please use the command below  
`main.exe -m "model\aclnet_des_53_fp32.xml" --audioname test.wav --input ju.mp4`

* `test.wav` will be generated,`timestamp.wav` and `timestamp.mp4` will also generated.

* Here is a sample of log results

```
[ INFO ] Creating Inference Engine
[ INFO ] Loading model model\aclnet_des_53_fp32.xml
[ INFO ] Loading model to the plugin
[ INFO ] Preparing input
use default speaker device for recording (Y or N):y
```
> if Y:

```
Selection is output. Using loopback mode.

Starting...
Press q to end the recoding
1669it [00:22, 85.12it/s]
q pressed, end recoding
1677it [00:23, 72.71it/s]
[ INFO ] Starting inference
[ INFO ] [0.00-0.33] - 77.18% Pig
[ INFO ] [0.33-0.67] - 40.01% Thunderstorm
[ INFO ] [0.67-1.00] - 92.83% Thunderstorm
[ INFO ] [1.00-1.33] - 94.67% Thunderstorm
[ INFO ] [1.33-1.67] - 99.29% Thunderstorm
[ INFO ] [1.67-2.00] - 76.73% Wind
[ INFO ] [2.00-2.33] - 99.95% Thunderstorm
[ INFO ] [2.33-2.67] - 97.18% Crackling fire
[ INFO ] [2.67-3.00] - 99.14% Wind
[ INFO ] [3.00-3.33] - 99.22% Thunderstorm
[ INFO ] [3.33-8.33] - 50.16% Gunshot File is saved.
[ INFO ] [9.00-9.33] - 64.26% Thunderstorm
```
> if N

```
Available devices:

0:       Microsoft Sound Mapper - Input
         MME

1:       Microphone Array (Realtek(R) Au
         MME

2:       Microsoft Sound Mapper - Output
         MME

3:       Speaker/HP (Realtek(R) Audio)
         MME

4:       Speaker/HP (Realtek(R) Audio)
         Windows WASAPI

5:       Microphone Array (Realtek(R) Audio)
         Windows WASAPI

6:       Speakers (Realtek HD Audio output)
         Windows WDM-KS

7:       Microphone Array (Realtek HD Audio Mic input)
         Windows WDM-KS

8:       Headphones ()
         Windows WDM-KS

9:       Headset (@System32\drivers\bthhfenum.sys,#2;%1 Hands-Free AG Audio%0
;(Adina’s AirPods Pro))
         Windows WDM-KS

10:      Headset (@System32\drivers\bthhfenum.sys,#2;%1 Hands-Free AG Audio%0
;(Adina’s AirPods Pro))
         Windows WDM-KS

11:      Headphones ()
         Windows WDM-KS

Choose device [{'index': 1, 'structVersion': 2, 'name': 'Microphone Array (Realtek(R) Au', 'hostApi': 0, 'maxInputChannels': 2, 'maxOutputChannels': 0, 'defaultLowInputLatency': 0.09, 'defaultLowOutputLatency': 0.09, 'defaultHighInputLatency': 0.18, 'defaultHighOutputLatency': 0.18, 'defaultSampleRate': 44100.0}]: 4

Selection is output. Using loopback mode.
```


* 打包exe

1. `pyinstaller main.py`
2. copy openvino folder
3. copy  follow dll file
```
	MKLDNNPlugin.dll
	plugins.xml
	inference_engine_ir_reader.dll
	inference_engine_lp_transformations.dll
```






























































































































