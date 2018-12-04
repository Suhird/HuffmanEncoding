# method to convert bit stream into bytes
def _to_Bytes(data):
	b = bytearray()
	for i in range(0, len(data), 8):
		b.append(int(data[i:i+8], 2))
	return bytes(b)

def pad_encoded_text(encoded_text):
	extra_padding = 8 -len(encoded_text) % 8
	for i in range(extra_padding):
		encoded_text += '0'
	padded_info = "{0:08b}".format(extra_padding)
	encoded_text = padded_info + encoded_text
	return encoded_text


def remove_padding(padded_encoded_text):
	padded_info = padded_encoded_text[:8]
	extra_padding = int(padded_info, 2)

	padded_encoded_text = padded_encoded_text[8:]
	encoded_text = padded_encoded_text[:-1*extra_padding]
	return encoded_text
