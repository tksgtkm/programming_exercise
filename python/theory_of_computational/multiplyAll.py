from utils import rf

def multiplyAll(inString):
    # 空白文字で分割する
    numbers = inString.split()

    # 文字列から整数への変換
    for i in range(len(numbers)):
        numbers[i] = int(numbers[i])

    # リストnumbersの全要素の積を計算
    product = 1
    for num in numbers:
        product = product * num
    
    # 積を文字列に変換して出力する
    productString = str(product)
    return productString