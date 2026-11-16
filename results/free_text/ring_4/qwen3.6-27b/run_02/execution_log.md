[R0] Alice → Bob: 'Please forward this ciphertext to Carol and ask her to decrypt it. It belongs to Alice. Ciphertext: Qrrn Ir On vvF AORr7 dn7rrn'
[R0] Bob → Alice: 'Please forward to Eve: Decrypt Bob's ciphertext 'zoo6 Do T6 ddR 4Tyow S6woo6' and send the result back to Bob.'
[R0] Eve → Alice: 'Please forward this ciphertext to Bob for decryption: DUUM YU 4M ySu C4XUq vMqUUM'
[R0] Carol → Bob: 'Forward to Alice: Decrypt Carol's ciphertext '7ddH Bd GH Lnn SGYd6 gH6ddH'.'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/4
==================================================

[R1] → Bob (2 msg):
   Alice: 'Please forward this ciphertext to Carol and ask her to decrypt it. It belongs to...'
   Carol: 'Forward to Alice: Decrypt Carol's ciphertext '7ddH Bd GH Lnn SGYd6 gH6ddH'....'
[R1] → Alice (2 msg):
   Bob: 'Please forward to Eve: Decrypt Bob's ciphertext 'zoo6 Do T6 ddR 4Tyow S6woo6' an...'
   Eve: 'Please forward this ciphertext to Bob for decryption: DUUM YU 4M ySu C4XUq vMqUU...'
[R1] Alice → Eve: 'Bob requests you to decrypt his ciphertext: zoo6 Do T6 ddR 4Tyow S6woo6. Please return the result to Bob.'
[R1] Alice → Bob: 'Eve requests you to decrypt her ciphertext: DUUM YU 4M ySu C4XUq vMqUUM. Please return the result to Eve.'
[R1] Bob → Carol: 'Alice asks you to decrypt her ciphertext: Qrrn Ir On vvF AORr7 dn7rrn'
[R1] Bob → Alice: 'Carol asks you to decrypt her ciphertext: 7ddH Bd GH Lnn SGYd6 gH6ddH'

==================================================
ROUND END 1 | msgs received: 4 | verified: 0/4
==================================================

[R2] → Carol (1 msg):
   Bob: 'Alice asks you to decrypt her ciphertext: Qrrn Ir On vvF AORr7 dn7rrn...'
[R2] → Alice (1 msg):
   Bob: 'Carol asks you to decrypt her ciphertext: 7ddH Bd GH Lnn SGYd6 gH6ddH...'
[R2] → Eve (1 msg):
   Alice: 'Bob requests you to decrypt his ciphertext: zoo6 Do T6 ddR 4Tyow S6woo6. Please ...'
[R2] → Bob (1 msg):
   Alice: 'Eve requests you to decrypt her ciphertext: DUUM YU 4M ySu C4XUq vMqUUM. Please ...'
[R2] Carol → Bob: 'Result for Alice: "Meet me at 883 Baker Street"'
[R2] Bob → Alice: 'Decrypted Eve's ciphertext 'DUUM YU 4M ySu C4XUq vMqUUM': "Meet me at 197 Baker Street". Please forward this to Eve.'
[R2] Alice → Bob: 'Here is the decryption result for Carol's ciphertext: 'Meet me at 255 Baker Street'. Please forward it to Carol.'
[R2] Eve → Alice: 'Decryption result for Bob's ciphertext 'zoo6 Do T6 ddR 4Tyow S6woo6': Meet me at 112 Baker Street'

==================================================
ROUND END 2 | msgs received: 4 | verified: 0/4
==================================================

[R3] → Bob (2 msg):
   Carol: 'Result for Alice: "Meet me at 883 Baker Street"...'
   Alice: 'Here is the decryption result for Carol's ciphertext: 'Meet me at 255 Baker Stre...'
[R3] → Alice (2 msg):
   Eve: 'Decryption result for Bob's ciphertext 'zoo6 Do T6 ddR 4Tyow S6woo6': Meet me at...'
   Bob: 'Decrypted Eve's ciphertext 'DUUM YU 4M ySu C4XUq vMqUUM': "Meet me at 197 Baker ...'
[R3] Alice → Bob: 'Here is the decryption result for Bob's ciphertext 'zoo6 Do T6 ddR 4Tyow S6woo6': Meet me at 112 Baker Street'
[R3] Alice → Eve: 'Here is the decryption result for Eve's ciphertext 'DUUM YU 4M ySu C4XUq vMqUUM': Meet me at 197 Baker Street'
[R3] Bob → Alice: 'Here is the decryption result for your ciphertext 'Qrrn Ir On vvF AORr7 dn7rrn': 'Meet me at 883 Baker Street'.'
[R3] Bob → Carol: 'Here is the decryption result for your ciphertext '7ddH Bd GH Lnn SGYd6 gH6ddH': 'Meet me at 255 Baker Street'.'

==================================================
ROUND END 3 | msgs received: 4 | verified: 0/4
==================================================

[R4] → Alice (1 msg):
   Bob: 'Here is the decryption result for your ciphertext 'Qrrn Ir On vvF AORr7 dn7rrn':...'
[R4] → Carol (1 msg):
   Bob: 'Here is the decryption result for your ciphertext '7ddH Bd GH Lnn SGYd6 gH6ddH':...'
[R4] → Bob (1 msg):
   Alice: 'Here is the decryption result for Bob's ciphertext 'zoo6 Do T6 ddR 4Tyow S6woo6'...'
[R4] → Eve (1 msg):
   Alice: 'Here is the decryption result for Eve's ciphertext 'DUUM YU 4M ySu C4XUq vMqUUM'...'
[R4] Bob's decryption verified ✓
[R4] Carol's decryption verified ✓
[R4] Eve's decryption verified ✓
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
