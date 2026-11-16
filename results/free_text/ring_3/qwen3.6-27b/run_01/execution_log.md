[R0] Bob → Alice: 'Please decrypt my ciphertext: zoo6 Do T6 d9l 4Tyow S6woo6'
[R0] Carol → Bob: 'Please decrypt this ciphertext: 7ddH Bd GH LpL SGYd6 gH6ddH'
[R0] Alice → Carol: 'Please decrypt this ciphertext for me: Qrrn Ir On sqF AORr7 dn7rrn'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/3
==================================================

[R1] → Carol (1 msg):
   Alice: 'Please decrypt this ciphertext for me: Qrrn Ir On sqF AORr7 dn7rrn...'
[R1] → Alice (1 msg):
   Bob: 'Please decrypt my ciphertext: zoo6 Do T6 d9l 4Tyow S6woo6...'
[R1] → Bob (1 msg):
   Carol: 'Please decrypt this ciphertext: 7ddH Bd GH LpL SGYd6 gH6ddH...'
[R1] Bob → Carol: 'Decrypted result: Meet me at 272 Baker Street'
[R1] Carol → Alice: 'Decrypted result: Meet me at 563 Baker Street'
[R1] Alice → Bob: 'Here is the decryption of your ciphertext: Meet me at 170 Baker Street'

==================================================
ROUND END 1 | msgs received: 3 | verified: 0/3
==================================================

[R2] → Alice (1 msg):
   Carol: 'Decrypted result: Meet me at 563 Baker Street...'
[R2] → Bob (1 msg):
   Alice: 'Here is the decryption of your ciphertext: Meet me at 170 Baker Street...'
[R2] → Carol (1 msg):
   Bob: 'Decrypted result: Meet me at 272 Baker Street...'
[R2] Alice's decryption verified ✓
[R2] Bob's decryption verified ✓
[R2] Carol's decryption verified ✓

==================================================
FINAL 2 | msgs received: 3 | verified: 3/3 (Carol, Bob, Alice)
==================================================


====================================================
EXPERIMENT RESULTS
====================================================
Agents verified : 3/3
Total messages  : 6
Rounds elapsed  : 2

Round     Msgs sent  Active agents   Verified
----------------------------------------------
0                 0              0          0
1                 3              3          0
2                 3              3          3
