"""
単純なランレングス符号化のプログラムを書いてください。
例えばBWWWWWBWWWWをより短い1B5W1B4Wに変換し、さらに圧縮した文字列を
もとの文字列に戻す復号化もできるようにしてください。
文字列を1パスで符号化と復号化ができるようにすべき。

str関数が数を文字列に変換する。例えばstr(12) = '12'
符号化に役立つ。
int関数は文字列を数値に変換する。int('12') = 12
任意の文字列sでs[i].isalpha()はs[i]が英字ならTrueを、それ以外ならFalseを返す。
s.isalpha()はsのすべての文字が英字ならTrueを返す。
関数intとisalphaは復号化で役立つ。
"""

strings = 'BWWWWWBWWWW'
print(strings)

def string_encoder(strings):
    s_count = 0
    encoder = []
    for i in range(len(strings)):
        if strings[0] != strings[i]:
            s = strings[i]
            s_count += 1
        else:
            s = strings[i]
            s_count += 1
        
        if i != len(strings) - 1:
            if strings[i] != strings[i+1]:
                encoder.append(s + str(s_count))
                s_count = 0
        else:
            encoder.append(s + str(s_count))
        
    encoding_string = ''
    for j in range(len(encoder)):
        encoding_string += encoder[j]
    
    return encoding_string

encoder = string_encoder(strings)
print(encoder)

def string_decoder(strings):
    decoder = []
    target_string_list = []
    string_volume_list = []
    string_volume = 0
    for i in range(len(strings)):
        if strings[i].isalpha():
            target_string = strings[i]
            target_string_list.append(target_string)
        else:
            string_volume = strings[i]
            string_volume_list.append(string_volume)
        
    for i, j in zip(target_string_list, string_volume_list):
        decode_string = i * int(j)
        decoder.append(decode_string)

    decoding_string = ''
    for j in range(len(decoder)):
        decoding_string += decoder[j]

    return decoding_string

decoder = string_decoder(encoder)
print(decoder)