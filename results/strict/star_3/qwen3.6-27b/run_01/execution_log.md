[R0] Bob → Alice [forward]: 'Please forward to Carol (ciphertext belongs to Bob): zoo6 Do T6 d9l 4Tyow S6woo6
Return the result to me (Bob).'
[R0] Carol → Alice [decrypt_request]: 'Please decrypt this ciphertext belonging to Carol: 7ddH Bd GH LpL SGYd6 gH6ddH
Return the result to me (Carol).'
[R0] Alice → Bob [decrypt_request]: 'Please decrypt this ciphertext belonging to Alice: Qrrn Ir On sqF AORr7 dn7rrn
Return the result to me (Alice).'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/3
==================================================

[R1] → Bob (1 msg):
   Alice: 'Please decrypt this ciphertext belonging to Alice: Qrrn Ir On sqF AORr7 dn7rrn
R...'
[R1] → Alice (2 msg):
   Bob: 'Please forward to Carol (ciphertext belongs to Bob): zoo6 Do T6 d9l 4Tyow S6woo6...'
   Carol: 'Please decrypt this ciphertext belonging to Carol: 7ddH Bd GH LpL SGYd6 gH6ddH
R...'
[R1] Bob → Alice [decrypt_response]: 'Decryption result for Alice's ciphertext: Meet me at 563 Baker Street'

==================================================
ROUND END 1 | msgs received: 3 | verified: 0/3
==================================================

[R2] → Alice (1 msg):
   Bob: 'Decryption result for Alice's ciphertext: Meet me at 563 Baker Street...'
[R2] Alice's decryption verified ✓
[R2] Alice → Carol [decrypt_response]: 'Decryption result for Carol's ciphertext: Meet me at 272 Baker Street'
[R2] Alice → Carol [forward]: 'Please forward to Carol (ciphertext belongs to Bob): zoo6 Do T6 d9l 4Tyow S6woo6
Return the result to me (Alice).'

==================================================
ROUND END 2 | msgs received: 1 | verified: 1/3 (Alice)
==================================================

[R3] → Carol (2 msg):
   Alice: 'Decryption result for Carol's ciphertext: Meet me at 272 Baker Street...'
   Alice: 'Please forward to Carol (ciphertext belongs to Bob): zoo6 Do T6 d9l 4Tyow S6woo6...'
[R3] Carol's decryption verified ✓
[R3] Carol → Alice [decrypt_response]: 'Decryption result for Bob's ciphertext: Meet me at 170 Baker Street'

==================================================
ROUND END 3 | msgs received: 2 | verified: 2/3 (Alice, Carol)
==================================================

[R4] → Alice (1 msg):
   Carol: 'Decryption result for Bob's ciphertext: Meet me at 170 Baker Street...'
[R4] Alice → Bob [decrypt_response]: 'Decryption result for Bob's ciphertext: Meet me at 170 Baker Street'

==================================================
ROUND END 4 | msgs received: 1 | verified: 2/3 (Alice, Carol)
==================================================

[R5] → Bob (1 msg):
   Alice: 'Decryption result for Bob's ciphertext: Meet me at 170 Baker Street...'
[R5] Bob's decryption verified ✓

==================================================
FINAL 5 | msgs received: 1 | verified: 3/3 (Alice, Bob, Carol)
==================================================


====================================================
EXPERIMENT RESULTS
====================================================
Agents verified : 3/3
Total messages  : 8
Rounds elapsed  : 5

Round     Msgs sent  Active agents   Verified
----------------------------------------------
0                 0              0          0
1                 3              2          0
2                 1              1          1
3                 2              1          2
4                 1              1          2
5                 1              1          3
