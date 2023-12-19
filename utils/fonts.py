bypass_fonts = {
    'a': '𝚊',
    'b': '𝚋',
    'c': '𝚌',
    'd': '𝚍',
    'e': '𝚎',
    'f': '𝚏',
    'g': '𝚐',
    'h': '𝚑',
    'i': '𝚒',
    'j': '𝚓',
    'k': '𝚔',
    'l': '𝚕',
    'm': '𝚖',
    'n': '𝚗',
    'o': '𝚘',
    'p': '𝚙',
    'q': '𝚚',
    'r': '𝚛',
    's': '𝚜',
    't': '𝚝',
    'u': '𝚞',
    'v': '𝚟',
    'w': '𝚠',
    'x': '𝚡',
    'y': '𝚢',
    'z': '𝚣'
}

regional_indicators = {
    'a': '<:regional_indicator_a:803940414524620800>',
    'b': '<:regional_indicator_b:803940414524620800>',
    'c': '<:regional_indicator_c:803940414524620800>',
    'd': '<:regional_indicator_d:803940414524620800>',
    'e': '<:regional_indicator_e:803940414524620800>',
    'f': '<:regional_indicator_f:803940414524620800>',
    'g': '<:regional_indicator_g:803940414524620800>',
    'h': '<:regional_indicator_h:803940414524620800>',
    'i': '<:regional_indicator_i:803940414524620800>',
    'j': '<:regional_indicator_j:803940414524620800>',
    'k': '<:regional_indicator_k:803940414524620800>',
    'l': '<:regional_indicator_l:803940414524620800>',
    'm': '<:regional_indicator_m:803940414524620800>',
    'n': '<:regional_indicator_n:803940414524620800>',
    'o': '<:regional_indicator_o:803940414524620800>',
    'p': '<:regional_indicator_p:803940414524620800>',
    'q': '<:regional_indicator_q:803940414524620800>',
    'r': '<:regional_indicator_r:803940414524620800>',
    's': '<:regional_indicator_s:803940414524620800>',
    't': '<:regional_indicator_t:803940414524620800>',
    'u': '<:regional_indicator_u:803940414524620800>',
    'v': '<:regional_indicator_v:803940414524620800>',
    'w': '<:regional_indicator_w:803940414524620800>',
    'x': '<:regional_indicator_x:803940414524620800>',
    'y': '<:regional_indicator_y:803940414524620800>',
    'z': '<:regional_indicator_z:803940414524620800>'
}

def bypass(text):
    text = text.lower()
    result = ""
    for char in text:
        if char in bypass_fonts:
            result += bypass_fonts[char]
        else:
            result += char
    return result

def regional(text):
    text = text.lower()
    result = ""
    for char in text:
        if char in regional_indicators:
            result += regional_indicators[char]
        else:
            result += char
    return result