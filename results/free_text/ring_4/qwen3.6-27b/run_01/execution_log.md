[R0] Alice → Bob: 'Bob, please forward my ciphertext 'Qrrn Ir On l8F AORr7 dn7rrn' to Carol and ask her to decrypt it. Once she replies, send the decryption result back to me.'
[R0] Bob → Alice: 'Please forward this ciphertext to Eve for decryption: 'zoo6 Do T6 9EF 4Tyow S6woo6'. It belongs to Bob. Return the result to me.'
[R0] Carol → Bob: 'Please forward to Alice: Decrypt Carol's ciphertext '7ddH Bd GH 8K1 SGYd6 gH6ddH'.'
[R0] Eve → Alice: 'Please forward to Bob and ask him to decrypt my ciphertext: DUUM YU 4M oP2 C4XUq vMqUUM. -Eve'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/4
==================================================

[R1] → Bob (2 msg):
   Alice: 'Bob, please forward my ciphertext 'Qrrn Ir On l8F AORr7 dn7rrn' to Carol and ask...'
   Carol: 'Please forward to Alice: Decrypt Carol's ciphertext '7ddH Bd GH 8K1 SGYd6 gH6ddH...'
[R1] → Alice (2 msg):
   Bob: 'Please forward this ciphertext to Eve for decryption: 'zoo6 Do T6 9EF 4Tyow S6wo...'
   Eve: 'Please forward to Bob and ask him to decrypt my ciphertext: DUUM YU 4M oP2 C4XUq...'
[R1] Alice → Eve: 'Bob requests that you decrypt this ciphertext: 'zoo6 Do T6 9EF 4Tyow S6woo6'. Please return the result to Alice.'
[R1] Alice → Bob: 'Eve requests that you decrypt this ciphertext: 'DUUM YU 4M oP2 C4XUq vMqUUM'. Please return the result to Alice.'
[R1] Bob → Carol: 'Please decrypt Alice's ciphertext 'Qrrn Ir On l8F AORr7 dn7rrn' and send the result back to me.'
[R1] Bob → Alice: 'Carol requests you to decrypt her ciphertext '7ddH Bd GH 8K1 SGYd6 gH6ddH' and send the result back to me.'

==================================================
ROUND END 1 | msgs received: 4 | verified: 0/4
==================================================

[R2] → Carol (1 msg):
   Bob: 'Please decrypt Alice's ciphertext 'Qrrn Ir On l8F AORr7 dn7rrn' and send the res...'
[R2] → Alice (1 msg):
   Bob: 'Carol requests you to decrypt her ciphertext '7ddH Bd GH 8K1 SGYd6 gH6ddH' and s...'
[R2] → Eve (1 msg):
   Alice: 'Bob requests that you decrypt this ciphertext: 'zoo6 Do T6 9EF 4Tyow S6woo6'. Pl...'
[R2] → Bob (1 msg):
   Alice: 'Eve requests that you decrypt this ciphertext: 'DUUM YU 4M oP2 C4XUq vMqUUM'. Pl...'
[R2] Eve → Alice: 'Decrypted result for Bob's request: 'Meet me at 746 Baker Street'. -Eve'
[R2] Carol → Bob: 'Decrypted Alice's ciphertext 'Qrrn Ir On l8F AORr7 dn7rrn': "Meet me at 413 Baker Street"'
[R2] Alice → Bob: 'The decryption of Carol's ciphertext '7ddH Bd GH 8K1 SGYd6 gH6ddH' is: 'Meet me at 348 Baker Street''
[R2] Bob → Alice: 'Here is the decryption result for Eve's ciphertext 'DUUM YU 4M oP2 C4XUq vMqUUM': "Meet me at 820 Baker Street". Please forward this to Eve.'

==================================================
ROUND END 2 | msgs received: 4 | verified: 0/4
==================================================

[R3] → Bob (2 msg):
   Carol: 'Decrypted Alice's ciphertext 'Qrrn Ir On l8F AORr7 dn7rrn': "Meet me at 413 Bake...'
   Alice: 'The decryption of Carol's ciphertext '7ddH Bd GH 8K1 SGYd6 gH6ddH' is: 'Meet me ...'
[R3] → Alice (2 msg):
   Eve: 'Decrypted result for Bob's request: 'Meet me at 746 Baker Street'. -Eve...'
   Bob: 'Here is the decryption result for Eve's ciphertext 'DUUM YU 4M oP2 C4XUq vMqUUM'...'
[R3] Bob → Alice: 'Carol decrypted your ciphertext 'Qrrn Ir On l8F AORr7 dn7rrn': "Meet me at 413 Baker Street"'
[R3] Bob → Carol: 'Alice decrypted your ciphertext '7ddH Bd GH 8K1 SGYd6 gH6ddH': 'Meet me at 348 Baker Street''
[R3] Alice → Bob: 'Here is the decryption result for your ciphertext 'zoo6 Do T6 9EF 4Tyow S6woo6' from Eve: 'Meet me at 746 Baker Street''
[R3] Alice → Eve: 'Here is the decryption result for your ciphertext 'DUUM YU 4M oP2 C4XUq vMqUUM' from Bob: 'Meet me at 820 Baker Street''

==================================================
ROUND END 3 | msgs received: 4 | verified: 0/4
==================================================

[R4] → Alice (1 msg):
   Bob: 'Carol decrypted your ciphertext 'Qrrn Ir On l8F AORr7 dn7rrn': "Meet me at 413 B...'
[R4] → Carol (1 msg):
   Bob: 'Alice decrypted your ciphertext '7ddH Bd GH 8K1 SGYd6 gH6ddH': 'Meet me at 348 B...'
[R4] → Bob (1 msg):
   Alice: 'Here is the decryption result for your ciphertext 'zoo6 Do T6 9EF 4Tyow S6woo6' ...'
[R4] → Eve (1 msg):
   Alice: 'Here is the decryption result for your ciphertext 'DUUM YU 4M oP2 C4XUq vMqUUM' ...'
[R4] Eve's decryption verified ✓
[R4] Carol's decryption verified ✓
[R4] Bob's decryption verified ✓
[R4] Alice's decryption verified ✓

==================================================
FINAL 4 | msgs received: 4 | verified: 4/4 (Carol, Bob, Eve, Alice)
==================================================


====================================================
EXPERIMENT RESULTS
====================================================
Agents verified : 4/4
Total messages  : 16
Rounds elapsed  : 4

Round     Msgs sent  Active agents   Verified
----------------------------------------------
0                 0              0          0
1                 4              2          0
2                 4              4          0
3                 4              2          0
4                 4              4          4
