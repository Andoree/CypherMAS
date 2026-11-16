[R0] Bob → Alice: 'Please ask Carol to decrypt this ciphertext for Bob: zoo6 Do T6 d9l 4Tyow S6woo6'
[R0] Carol → Alice: 'Please decrypt my ciphertext: 7ddH Bd GH LpL SGYd6 gH6ddH'
[R0] Alice → Bob: 'Please decrypt my ciphertext: Qrrn Ir On sqF AORr7 dn7rrn'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/3
==================================================

[R1] → Bob (1 msg):
   Alice: 'Please decrypt my ciphertext: Qrrn Ir On sqF AORr7 dn7rrn...'
[R1] → Alice (2 msg):
   Bob: 'Please ask Carol to decrypt this ciphertext for Bob: zoo6 Do T6 d9l 4Tyow S6woo6...'
   Carol: 'Please decrypt my ciphertext: 7ddH Bd GH LpL SGYd6 gH6ddH...'
[R1] Bob → Alice: 'Decrypted result for Alice: Meet me at 563 Baker Street'
[R1] Alice → Carol: 'Decryption result for your ciphertext 7ddH Bd GH LpL SGYd6 gH6ddH: Meet me at 272 Baker Street'
[R1] Alice → Carol: 'Bob asks you to decrypt this ciphertext: zoo6 Do T6 d9l 4Tyow S6woo6'

==================================================
ROUND END 1 | msgs received: 3 | verified: 0/3
==================================================

[R2] → Alice (1 msg):
   Bob: 'Decrypted result for Alice: Meet me at 563 Baker Street...'
[R2] → Carol (2 msg):
   Alice: 'Decryption result for your ciphertext 7ddH Bd GH LpL SGYd6 gH6ddH: Meet me at 27...'
   Alice: 'Bob asks you to decrypt this ciphertext: zoo6 Do T6 d9l 4Tyow S6woo6...'
[R2] Alice's decryption verified ✓
[R2] Carol's decryption verified ✓
[R2] Carol → Alice: 'Decryption result for Bob's ciphertext zoo6 Do T6 d9l 4Tyow S6woo6: Meet me at 170 Baker Street. Please forward to Bob.'

==================================================
ROUND END 2 | msgs received: 3 | verified: 2/3 (Carol, Alice)
==================================================

[R3] → Alice (1 msg):
   Carol: 'Decryption result for Bob's ciphertext zoo6 Do T6 d9l 4Tyow S6woo6: Meet me at 1...'
[R3] Alice → Bob: 'Carol decrypted your ciphertext zoo6 Do T6 d9l 4Tyow S6woo6: Meet me at 170 Baker Street'

==================================================
ROUND END 3 | msgs received: 1 | verified: 2/3 (Carol, Alice)
==================================================

[R4] → Bob (1 msg):
   Alice: 'Carol decrypted your ciphertext zoo6 Do T6 d9l 4Tyow S6woo6: Meet me at 170 Bake...'
[R4] Bob's decryption verified ✓

==================================================
FINAL 4 | msgs received: 1 | verified: 3/3 (Carol, Bob, Alice)
==================================================


====================================================
EXPERIMENT RESULTS
====================================================
Agents verified : 3/3
Total messages  : 8
Rounds elapsed  : 4

Round     Msgs sent  Active agents   Verified
----------------------------------------------
0                 0              0          0
1                 3              2          0
2                 3              2          2
3                 1              1          2
4                 1              1          3
