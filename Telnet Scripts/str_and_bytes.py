s1 = 'abc'

# encoding str to bytes
b1 = s1.encode('utf-8')
print(type(b1)) # => <class 'bytes'>


print(b1[0])    # => 97
print(b1[1])    # => 98

print(b1)   # => b'abc'

s2 = 'ハッキング'   # non-ascii string

# encoding to bytes
b2 = s2.encode()
print(b2)   # => b'\xe3\x83\x8f\xe3\x83\x83\xe3\x82\xad\xe3\x83\xb3\xe3\x82\xb0'

print(b2[0])    # => 227

# decoding back to str
s3 = b2.decode()
print(s3, s3 == s2) # => ハッキング True