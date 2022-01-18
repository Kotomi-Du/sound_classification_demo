#!/usr/bin/env python3
"""
 Copyright (C) 2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from argparse import ArgumentParser, SUPPRESS
import logging
import sys
import time
import wave

import numpy as np
from openvino.inference_engine import IECore
import sound_record



class AudioSource:
    def __init__(self, source, channels=2, samplerate=None):
        self.samplerate = samplerate
        #samplerate, audio, self.origin_data = read_wav(source, as_float=True)
        samplerate, audio, self.origin_data  = sound_record.start_record(source)
        #print(audio.shape, samplerate, self.samplerate)
        audio = audio.T
        if audio.shape[0] != channels:
            raise RuntimeError("Audio has unsupported number of channels - {} (expected {})"
                               .format(audio.shape[0], channels))
        if self.samplerate:
            if self.samplerate != samplerate:
                audio = resample(audio, samplerate, self.samplerate)
        else:
            self.samplerate = samplerate

        self.audio = audio
        

    def duration(self):
        return self.audio.shape[1] / self.samplerate

    def chunks(self, size, hop=None, num_chunks=1):
        def get_clip(pos, size):
            if pos > self.audio.shape[1]:
                return np.zeros((self.audio.shape[0], size), dtype=self.audio.dtype)
            if pos + size > self.audio.shape[1]:
                clip = np.zeros((self.audio.shape[0], size), dtype=self.audio.dtype)
                clip[:, :self.audio.shape[1]-pos] = self.audio[:, pos:]
                return clip
            else:
                return self.audio[:, pos:pos+size]
        if not hop:
            hop = size
        pos = 0

        while pos < self.audio.shape[1]:
            chunk = np.zeros((num_chunks, self.audio.shape[0], size), dtype=self.audio.dtype)
            for n in range(num_chunks):
                chunk[n, :, :] = get_clip(pos, size)
                pos += hop
            yield chunk


def resample(audio, sample_rate, new_sample_rate):
    duration = audio.shape[1] / float(sample_rate)
    x_old = np.linspace(0, duration, audio.shape[1])
    x_new = np.linspace(0, duration, int(duration*new_sample_rate))
    data = np.array([np.interp(x_new, x_old, channel) for channel in audio])

    return data


def read_wav(file, as_float=False):
    sampwidth_types = {
        1: np.uint8,
        2: np.int16,
        4: np.int32
    }

    with wave.open(file, "rb") as wav:
        params = wav.getparams()
        data = wav.readframes(params.nframes)
        if params.sampwidth in sampwidth_types:
            data = np.frombuffer(data, dtype=sampwidth_types[params.sampwidth])
        else:
            raise RuntimeError("Couldn't process file {}: unsupported sample width {}"
                               .format(file, params.sampwidth))
        data = np.reshape(data, (params.nframes, params.nchannels))
        if params.nchannels == 2:
            data = data[:,0]
            data = data[:,np.newaxis]
        if as_float:
            origin_data = data
            data = (data - np.mean(data)) / (np.std(data) + 1e-15)

    return params.framerate, data, origin_data

