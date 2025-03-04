import pyttsx3
engine = pyttsx3.init()


engine.save_to_file('Hello, this is a test audio file.', 'test_audio.wav')
engine.runAndWait()
print("语音文件已生成: test_audio.wav")


voices = engine.getProperty('voices')
for voice in voices:
    print(voice.languages)
    if voice.languages and 'zh' in voice.languages[0].decode('utf-8'):
        engine.setProperty('voice', voice.id)
        break
engine.save_to_file('我打起精神，走出门外，走进了那条小路，走到荷塘旁。'
                    '月光如流水般洒在荷塘上，波光粼粼，像是洒落在水面上的银沙。'
                    '我站在桥头，低头看着那浮动的月光，心里渐渐有了些许宁静。'
                    '荷叶上布满了晶莹的露珠，月光打在露珠上，像是给荷叶披上了一层薄薄的银纱。'
                    '偶尔有微风吹过，荷叶轻轻摇动，露珠像珠子般滚落到水面，荡起涟漪。'
                    '我想，这样的月光、荷塘，静静地、深深地进入了我的心中，所有的喧嚣、烦扰，都暂时被抛在了脑后。'
                    '夜晚的凉爽与清新，带来了无尽的遐想和深思。', 'test_audio_chinese.wav')
engine.runAndWait()
print("中文语音文件已生成: test_audio_chinese.wav")
