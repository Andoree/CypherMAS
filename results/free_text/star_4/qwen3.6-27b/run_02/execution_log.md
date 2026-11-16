[R0] Alice → Bob: 'Please decrypt my ciphertext: Qrrn Ir On vvF AORr7 dn7rrn'
[R0] Eve → Alice: 'I am Eve. Please decrypt my ciphertext: DUUM YU 4M ySu C4XUq vMqUUM'
[R0] Carol → Alice: 'Alice, please forward this request to Eve: Decrypt Carol's ciphertext '7ddH Bd GH Lnn SGYd6 gH6ddH'. Only Eve can decrypt it.'
[R0] Bob → Alice: 'Please relay to Carol: Decrypt my ciphertext: zoo6 Do T6 ddR 4Tyow S6woo6'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/4
==================================================

[R1] → Bob (1 msg):
   Alice: 'Please decrypt my ciphertext: Qrrn Ir On vvF AORr7 dn7rrn...'
[R1] → Alice (3 msg):
   Bob: 'Please relay to Carol: Decrypt my ciphertext: zoo6 Do T6 ddR 4Tyow S6woo6...'
   Carol: 'Alice, please forward this request to Eve: Decrypt Carol's ciphertext '7ddH Bd G...'
   Eve: 'I am Eve. Please decrypt my ciphertext: DUUM YU 4M ySu C4XUq vMqUUM...'
[R1] Bob → Alice: 'Decrypted result: Meet me at 883 Baker Street'
[R1] Alice → Eve: 'Here is the decryption of your ciphertext: Meet me at 197 Baker Street'
[R1] Alice → Carol: 'Relaying from Bob: Please decrypt my ciphertext: zoo6 Do T6 ddR 4Tyow S6woo6'
[R1] Alice → Eve: 'Relaying from Carol: Please decrypt her ciphertext '7ddH Bd GH Lnn SGYd6 gH6ddH'. Only you can decrypt it.'

==================================================
ROUND END 1 | msgs received: 4 | verified: 0/4
==================================================

[R2] → Alice (1 msg):
   Bob: 'Decrypted result: Meet me at 883 Baker Street...'
[R2] → Eve (2 msg):
   Alice: 'Here is the decryption of your ciphertext: Meet me at 197 Baker Street...'
   Alice: 'Relaying from Carol: Please decrypt her ciphertext '7ddH Bd GH Lnn SGYd6 gH6ddH'...'
[R2] → Carol (1 msg):
   Alice: 'Relaying from Bob: Please decrypt my ciphertext: zoo6 Do T6 ddR 4Tyow S6woo6...'
[R2] Alice's decryption verified ✓
[R2] Alice → Bob: 'Thank you, Bob! My ciphertext has been successfully decrypted.'
[R2] Eve's decryption verified ✓
[R2] Carol → Alice: 'Alice, please relay to Bob: The decryption of 'zoo6 Do T6 ddR 4Tyow S6woo6' is 'Meet me at 112 Baker Street'.'
[R2] Eve's decryption verified ✓
[R2] Eve → Alice: 'Decryption for Carol's ciphertext '7ddH Bd GH Lnn SGYd6 gH6ddH' is: Meet me at 255 Baker Street'

==================================================
ROUND END 2 | msgs received: 4 | verified: 2/4 (Eve, Alice)
==================================================

[R3] → Bob (1 msg):
   Alice: 'Thank you, Bob! My ciphertext has been successfully decrypted....'
[R3] → Alice (2 msg):
   Eve: 'Decryption for Carol's ciphertext '7ddH Bd GH Lnn SGYd6 gH6ddH' is: Meet me at 2...'
   Carol: 'Alice, please relay to Bob: The decryption of 'zoo6 Do T6 ddR 4Tyow S6woo6' is '...'
[R3] Alice → Carol: 'Relaying from Eve: The decryption for your ciphertext '7ddH Bd GH Lnn SGYd6 gH6ddH' is: Meet me at 255 Baker Street'
[R3] Alice → Bob: 'Relaying from Carol: The decryption of 'zoo6 Do T6 ddR 4Tyow S6woo6' is 'Meet me at 112 Baker Street'.'

==================================================
ROUND END 3 | msgs received: 3 | verified: 2/4 (Eve, Alice)
==================================================

[R4] → Carol (1 msg):
   Alice: 'Relaying from Eve: The decryption for your ciphertext '7ddH Bd GH Lnn SGYd6 gH6d...'
[R4] → Bob (1 msg):
   Alice: 'Relaying from Carol: The decryption of 'zoo6 Do T6 ddR 4Tyow S6woo6' is 'Meet me...'
[R4] Carol's decryption verified ✓
[R4] Bob's decryption verified ✓

==================================================
FINAL 4 | msgs received: 2 | verified: 4/4 (Carol, Bob, Eve, Alice)
==================================================


====================================================
EXPERIMENT RESULTS
====================================================
Agents verified : 4/4
Total messages  : 13
Rounds elapsed  : 4

Round     Msgs sent  Active agents   Verified
----------------------------------------------
0                 0              0          0
1                 4              2          0
2                 4              3          2
3                 3              2          2
4                 2              2          4
