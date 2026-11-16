[R0] Carol → Bob [forward]: 'Please forward to Alice (ciphertext belongs to Carol): 7ddH Bd GH 8K1 SGYd6 gH6ddH
Return the result to me (Carol).'
[R0] Bob → Alice [forward]: 'Please forward to Eve (ciphertext belongs to Bob): zoo6 Do T6 9EF 4Tyow S6woo6
Return the result to me (Bob).'
[R0] Alice → Bob [forward]: 'Please forward to Carol (ciphertext belongs to Alice): Qrrn Ir On l8F AORr7 dn7rrn
Return the result to me (Alice).'
[R0] Eve → Alice [forward]: 'Please forward to Bob (ciphertext belongs to Eve): DUUM YU 4M oP2 C4XUq vMqUUM
Return the result to me (Eve).'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/4
==================================================

[R1] → Bob (2 msg):
   Alice: 'Please forward to Carol (ciphertext belongs to Alice): Qrrn Ir On l8F AORr7 dn7r...'
   Carol: 'Please forward to Alice (ciphertext belongs to Carol): 7ddH Bd GH 8K1 SGYd6 gH6d...'
[R1] → Alice (2 msg):
   Bob: 'Please forward to Eve (ciphertext belongs to Bob): zoo6 Do T6 9EF 4Tyow S6woo6
R...'
   Eve: 'Please forward to Bob (ciphertext belongs to Eve): DUUM YU 4M oP2 C4XUq vMqUUM
R...'
[R1] Bob → Carol [decrypt_request]: 'Please decrypt this ciphertext belonging to Alice: Qrrn Ir On l8F AORr7 dn7rrn
Return the result to me (Bob).'
[R1] Bob → Alice [decrypt_request]: 'Please decrypt this ciphertext belonging to Carol: 7ddH Bd GH 8K1 SGYd6 gH6ddH
Return the result to me (Bob).'
[R1] Alice → Eve [decrypt_request]: 'Please decrypt this ciphertext belonging to Bob: zoo6 Do T6 9EF 4Tyow S6woo6
Return the result to me (Alice).'
[R1] Alice → Bob [decrypt_request]: 'Please decrypt this ciphertext belonging to Eve: DUUM YU 4M oP2 C4XUq vMqUUM
Return the result to me (Alice).'

==================================================
ROUND END 1 | msgs received: 4 | verified: 0/4
==================================================

[R2] → Carol (1 msg):
   Bob: 'Please decrypt this ciphertext belonging to Alice: Qrrn Ir On l8F AORr7 dn7rrn
R...'
[R2] → Alice (1 msg):
   Bob: 'Please decrypt this ciphertext belonging to Carol: 7ddH Bd GH 8K1 SGYd6 gH6ddH
R...'
[R2] → Eve (1 msg):
   Alice: 'Please decrypt this ciphertext belonging to Bob: zoo6 Do T6 9EF 4Tyow S6woo6
Ret...'
[R2] → Bob (1 msg):
   Alice: 'Please decrypt this ciphertext belonging to Eve: DUUM YU 4M oP2 C4XUq vMqUUM
Ret...'
[R2] Alice → Bob [decrypt_response]: 'Decryption result for Carol's ciphertext: Meet me at 348 Baker Street'
[R2] Bob → Alice [decrypt_response]: 'Decryption result for Eve's ciphertext: Meet me at 820 Baker Street'
[R2] Eve → Alice [decrypt_response]: 'Decryption result for Bob's ciphertext: Meet me at 746 Baker Street'
[R2] Carol → Bob [decrypt_response]: 'Decryption result for Alice's ciphertext: Meet me at 413 Baker Street'

==================================================
ROUND END 2 | msgs received: 4 | verified: 0/4
==================================================

[R3] → Bob (2 msg):
   Carol: 'Decryption result for Alice's ciphertext: Meet me at 413 Baker Street...'
   Alice: 'Decryption result for Carol's ciphertext: Meet me at 348 Baker Street...'
[R3] → Alice (2 msg):
   Eve: 'Decryption result for Bob's ciphertext: Meet me at 746 Baker Street...'
   Bob: 'Decryption result for Eve's ciphertext: Meet me at 820 Baker Street...'
[R3] Alice → Bob [decrypt_response]: 'Decryption result for Bob's ciphertext: Meet me at 746 Baker Street'
[R3] Alice → Eve [decrypt_response]: 'Decryption result for Eve's ciphertext: Meet me at 820 Baker Street'
[R3] Bob → Alice [decrypt_response]: 'Decryption result for Alice's ciphertext: Meet me at 413 Baker Street'
[R3] Bob → Carol [decrypt_response]: 'Decryption result for Carol's ciphertext: Meet me at 348 Baker Street'

==================================================
ROUND END 3 | msgs received: 4 | verified: 0/4
==================================================

[R4] → Alice (1 msg):
   Bob: 'Decryption result for Alice's ciphertext: Meet me at 413 Baker Street...'
[R4] → Carol (1 msg):
   Bob: 'Decryption result for Carol's ciphertext: Meet me at 348 Baker Street...'
[R4] → Bob (1 msg):
   Alice: 'Decryption result for Bob's ciphertext: Meet me at 746 Baker Street...'
[R4] → Eve (1 msg):
   Alice: 'Decryption result for Eve's ciphertext: Meet me at 820 Baker Street...'
[R4] Carol's decryption verified ✓
[R4] Bob's decryption verified ✓
[R4] Eve's decryption verified ✓
[R4] Alice's decryption verified ✓

==================================================
FINAL 4 | msgs received: 4 | verified: 4/4 (Alice, Bob, Eve, Carol)
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
