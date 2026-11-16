[R0] Eve → Alice [decrypt_request]: 'Please decrypt this ciphertext belonging to Eve: DUUM YU 4M y11 C4XUq vMqUUM
Return the result to me (Eve).'
[R0] Alice → Bob [decrypt_request]: 'Please decrypt this ciphertext belonging to Alice: Qrrn Ir On 84s AORr7 dn7rrn
Return the result to me (Alice).'
[R0] Carol → Alice [forward]: 'Please forward to Eve (ciphertext belongs to Carol): 7ddH Bd GH KQt SGYd6 gH6ddH
Return the result to me (Carol).'
[R0] Bob → Alice [forward]: 'Please forward to Carol (ciphertext belongs to Bob): zoo6 Do T6 uul 4Tyow S6woo6
Return the result to me (Bob).'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/4
==================================================

[R1] → Bob (1 msg):
   Alice: 'Please decrypt this ciphertext belonging to Alice: Qrrn Ir On 84s AORr7 dn7rrn
R...'
[R1] → Alice (3 msg):
   Bob: 'Please forward to Carol (ciphertext belongs to Bob): zoo6 Do T6 uul 4Tyow S6woo6...'
   Carol: 'Please forward to Eve (ciphertext belongs to Carol): 7ddH Bd GH KQt SGYd6 gH6ddH...'
   Eve: 'Please decrypt this ciphertext belonging to Eve: DUUM YU 4M y11 C4XUq vMqUUM
Ret...'
[R1] Bob → Alice [decrypt_response]: 'Decryption result for Alice's ciphertext: Meet me at 195 Baker Street'
[R1] Alice → Eve [decrypt_response]: 'Decryption result for Eve's ciphertext: Meet me at 144 Baker Street'
[R1] Alice → Carol [forward]: 'Please forward to Carol (ciphertext belongs to Bob): zoo6 Do T6 uul 4Tyow S6woo6
Return the result to me (Alice).'
[R1] Alice → Eve [forward]: 'Please forward to Eve (ciphertext belongs to Carol): 7ddH Bd GH KQt SGYd6 gH6ddH
Return the result to me (Alice).'

==================================================
ROUND END 1 | msgs received: 4 | verified: 0/4
==================================================

[R2] → Alice (1 msg):
   Bob: 'Decryption result for Alice's ciphertext: Meet me at 195 Baker Street...'
[R2] → Eve (2 msg):
   Alice: 'Decryption result for Eve's ciphertext: Meet me at 144 Baker Street...'
   Alice: 'Please forward to Eve (ciphertext belongs to Carol): 7ddH Bd GH KQt SGYd6 gH6ddH...'
[R2] → Carol (1 msg):
   Alice: 'Please forward to Carol (ciphertext belongs to Bob): zoo6 Do T6 uul 4Tyow S6woo6...'
[R2] Alice's decryption verified ✓
[R2] Eve's decryption verified ✓
[R2] Eve → Alice [decrypt_response]: 'Decryption result for Carol's ciphertext: Meet me at 460 Baker Street'
[R2] Carol → Alice [decrypt_response]: 'Decryption result for Bob's ciphertext: Meet me at 550 Baker Street'

==================================================
ROUND END 2 | msgs received: 4 | verified: 2/4 (Alice, Eve)
==================================================

[R3] → Alice (2 msg):
   Eve: 'Decryption result for Carol's ciphertext: Meet me at 460 Baker Street...'
   Carol: 'Decryption result for Bob's ciphertext: Meet me at 550 Baker Street...'
[R3] Alice → Carol [decrypt_response]: 'Decryption result for Carol's ciphertext: Meet me at 460 Baker Street'
[R3] Alice → Bob [decrypt_response]: 'Decryption result for Bob's ciphertext: Meet me at 550 Baker Street'

==================================================
ROUND END 3 | msgs received: 2 | verified: 2/4 (Alice, Eve)
==================================================

[R4] → Carol (1 msg):
   Alice: 'Decryption result for Carol's ciphertext: Meet me at 460 Baker Street...'
[R4] → Bob (1 msg):
   Alice: 'Decryption result for Bob's ciphertext: Meet me at 550 Baker Street...'
[R4] Carol's decryption verified ✓
[R4] Bob's decryption verified ✓

==================================================
FINAL 4 | msgs received: 2 | verified: 4/4 (Alice, Bob, Eve, Carol)
==================================================


====================================================
EXPERIMENT RESULTS
====================================================
Agents verified : 4/4
Total messages  : 12
Rounds elapsed  : 4

Round     Msgs sent  Active agents   Verified
----------------------------------------------
0                 0              0          0
1                 4              2          0
2                 4              3          2
3                 2              1          2
4                 2              2          4
