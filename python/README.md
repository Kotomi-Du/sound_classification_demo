* Please use the command below 
`main.exe -m "model\aclnet_des_53_fp32.xml" --audioname test.wav --input ju.mp4`

* test.wav will be generate as well as the log below
[ INFO ] Creating Inference Engine
[ INFO ] Loading model C:\Users\yarudu\OneDrive - Intel Corporation\Documents\project\sound_classification_demo\python\model\aclnet_des_53_fp32.xml
[ INFO ] Loading model to the plugin
[ INFO ] Preparing input
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

Record time in seconds [5]: 10
48000.0
Starting...
100%|████████████████████████████████████████████████████████████████████████████████| 937/937 [00:09<00:00, 93.70it/s]
End.
[ INFO ] Starting inference
[ INFO ] [0.00-0.33] - 37.33% Wind
[ INFO ] [0.33-0.67] - 91.79% Door knock
[ INFO ] [0.67-1.00] - 56.38% Airplane
[ INFO ] [1.00-1.33] - 83.01% Wind
[ INFO ] [1.33-1.67] - 49.53% Wind
[ INFO ] [1.67-2.00] - 92.53% Thunderstorm
[ INFO ] [2.00-2.33] - 98.89% Thunderstorm
[ INFO ] [2.33-2.67] - 99.93% Fireworks
[ INFO ] [2.67-3.00] - 36.80% Wind
[ INFO ] [3.00-3.33] - 94.04% Airplane
[ INFO ] [3.33-3.67] - 84.29% Fireworks
[ INFO ] [3.67-4.00] - 59.82% Airplane
[ INFO ] [4.00-4.33] - 99.81% Wind
[ INFO ] [4.33-4.67] - 97.00% Wind
[ INFO ] [4.67-5.00] - 85.25% Airplane
[ INFO ] [5.00-5.33] - 98.87% Train
[ INFO ] [5.33-5.67] - 37.28% Door knock
[ INFO ] [5.67-6.00] - 86.30% Airplane
[ INFO ] [6.00-6.33] - 99.32% Crowd
[ INFO ] [6.33-6.67] - 99.90% Gunshot
[ INFO ] [8.33-8.67] - 89.39% Thunderstorm
[ INFO ] [8.67-9.00] - 48.81% Fireworks
[ INFO ] [9.00-9.33] - 81.33% Thunderstorm
[ INFO ] [9.33-9.67] - 95.89% Thunderstorm
[ INFO ] [9.67-10.00] - 86.43% Airplane


































































































































