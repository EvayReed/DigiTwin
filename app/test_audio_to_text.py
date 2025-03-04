
# 结论:
# google_speech_recognition 识别准确 支持中英文  免费API有次数限制
# vosk 免费 支持各种语言包括方言 识别准确 有各种不同大小预训练好的模型
# deepspeech 最高支持python3.8 不太建议
# whisper openAI的接口 非常好用 不免费
# pocketsphinx 识别中文不太行
# PaddleSpeech python3.12 不支持3.13 功能比较多 挺好用 不过这个安装有点复杂



# Google Speech Recognition (SpeechRecognition)
# 简介: 这是一个非常受欢迎的 Python 库，支持多种语音识别引擎，包括 Google Web Speech API、CMU Sphinx、Google Cloud Speech 等。
# 其内置的 Google Web Speech API 是免费的，但有调用次数限制。
# 优点: 易于使用，支持多个引擎，能够处理不同语言。
# 安装: pip install SpeechRecognition

#  Google Web Speech API（免费）
# 每日调用限制：Google 的 Web Speech API 免费版本通常每天最多可以进行 50次请求。
# 请求限制：每个请求的音频长度有限制，通常最大可以识别 1分钟左右 的音频内容。

def use_google_speech_recognition(file_path, language):
    import speech_recognition as sr
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        if language == 'english':
            text = recognizer.recognize_google(audio)
        if language == 'chinese':
            text = recognizer.recognize_google(audio, language="zh-CN")
        print("Text:", text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError:
        print("API request error")

# Vosk
# 简介: Vosk 是一个非常强大的开源离线语音识别工具，支持多种语言，适用于需要离线语音识别的场景。它可以在低资源设备上运行，支持 Python 和其他语言的接口。
# 优点: 离线支持，准确度高，支持多种语言和方言。
# 安装: pip install vosk

# https://alphacephei.com/vosk/models 下载模型到本地

def use_vosk(file_path, language):
    from vosk import Model, KaldiRecognizer
    import wave
    if language == 'english':
        model = Model(model_path="D:\\vosk-model-small-en-us-0.15")
    if language == 'chinese':
        model = Model(model_path="D:\\vosk-model-small-cn-0.22")
    wf = wave.open(file_path, "rb")
    recognizer = KaldiRecognizer(model, wf.getframerate())

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            print(recognizer.Result())
    print(recognizer.Result())



# 3. DeepSpeech
# 简介: 由 Mozilla 开发的 DeepSpeech 是一个开源的语音识别框架，基于深度学习技术。DeepSpeech 可以离线运行，且支持多种语言模型。
# 优点: 高准确率，开源且可定制，适合开发者进行深度优化和训练。
# 安装: pip install deepspeech

# python最高3.8
# https://github.com/mozilla/DeepSpeech/releases 下载模型到本地


def use_deepspeech(file_path, language):
    import deepspeech
    import wave
    import numpy as np

    if language == 'english':
        model_path = 'D:\\deepspeech-0.9.3-models.pbmm'
        scorer_file_path = "D:\\deepspeech-0.9.3-models.scorer"
    if language == 'chinese':
        model_path = 'D:\\deepspeech-0.9.3-models-zh-CN.pbmm'
        scorer_file_path = "D:\\deepspeech-0.9.3-models-zh-CN.scorer"

    model = deepspeech.Model(model_path)
    model.enableExternalScorer(scorer_file_path)
    wf = wave.open(file_path, "rb")

    frames = wf.readframes(wf.getnframes())
    audio_data = np.frombuffer(frames, dtype=np.int16)
    text = model.stt(audio_data)
    print(text)



# 4. Whisper (by OpenAI)
# 简介: Whisper 是 OpenAI提供的一个自动语音识别（ASR）系统，支持多种语言的语音转文本。其特别之处在于能够处理多种语言和口音，且可以在各种噪声环境下提供不错的表现。
# 优点: 精度高，支持多语言，开源。
# 安装: pip install openai-whisper

# https://github.com/openai/whisper/releases 下载模型地址

def use_whisper(file_path, language):
    from openai import OpenAI
    client = OpenAI(api_key="")
    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    print(transcription.text)


# 5. CMU Sphinx (pocketsphinx)
# 安装: pip install pocketsphinx

# 准确性较低：相比于 Vosk，PocketSphinx 的识别准确性较差，特别是在噪声较大的环境下。
# 语言支持有限：PocketSphinx 的语言支持相对较少，主要是英文，对于其他语言的支持较差，尤其是中文。

def use_pocketsphinx(file_path, language):
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_sphinx(audio)
        print("Recognized text:", text)
    except sr.UnknownValueError:
        print("Sphinx could not understand the audio")
    except sr.RequestError:
        print("Sphinx request error")



# PaddleSpeech  python3.12 3.13×
# https://github.com/PaddlePaddle/PaddleSpeech/blob/develop/README_cn.md

def use_PaddleSpeech(file_path, language):
    from PaddleSpeech.paddlespeech.cli.asr.infer import ASRExecutor
    from PaddleSpeech.paddlespeech.cli.text.infer import TextExecutor

    asr = ASRExecutor()
    if language == 'english':
        result = asr(model='transformer_librispeech', audio_file=file_path, lang='en')
        print(result)
    if language == 'chinese':
        result = asr(audio_file=file_path, lang='zh')
        print(result)
        text_punc = TextExecutor()
        result = text_punc(text=result)
        print(result)



# 结论:
# 好用但不免费: whisper(openAI)、google_speech
# 好用、免费、但配置调试好需要付出点精力: vosk PaddleSpeech
# 不太适合用: deepspeech pocketsphinx

# google_speech_recognition 识别准确 支持中英文  免费API有次数限制
# vosk 免费 支持各种语言包括方言 识别准确 有各种不同大小预训练好的模型
# deepspeech 最高支持python3.8 不太建议
# whisper openAI的接口 非常好用 不免费
# pocketsphinx 识别中文不太行 排除
# PaddleSpeech python3.12 不支持3.13 功能比较多 挺好用 不过这个安装有点复杂



# 测试 'deepspeech' 虚拟环境 python3.8
# 测试 'PaddleSpeech' 虚拟环境 python3.12
# 测试 'google_speech_recognition', 'vosk', ''whisper', 'pocketsphinx' 虚拟环境 python3.13

import sys
python_version = sys.version_info

if python_version.major == 3 and python_version.minor == 13:
    for method in ['google_speech_recognition', 'vosk', 'whisper', 'pocketsphinx']:
        try:
            print('--------------------', method, '--------------------')
            eval('use_' + method)('test_audio.wav', 'english')
            eval('use_' + method)('test_audio_chinese.wav', 'chinese')
        except Exception as e:
            print(method + " Error: " + str(e))
elif python_version.major == 3 and python_version.minor == 12:
    for method in ['PaddleSpeech']:
        try:
            print('--------------------', method, '--------------------')
            eval('use_' + method)('test_audio.wav', 'english')
            eval('use_' + method)('test_audio_chinese.wav', 'chinese')
        except Exception as e:
            print(method + " Error: " + str(e))
elif python_version.major == 3 and python_version.minor == 8:
    for method in ['deepspeech']:
        try:
            print('--------------------', method, '--------------------')
            eval('use_' + method)('test_audio.wav', 'english')
            eval('use_' + method)('test_audio_chinese.wav', 'chinese')
        except Exception as e:
            print(method + " Error: " + str(e))
else:
    print(f"Other Python version: {python_version.major}.{python_version.minor}")






