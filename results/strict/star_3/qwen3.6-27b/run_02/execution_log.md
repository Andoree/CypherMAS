[R0] Bob → Alice [forward]: 'Please forward to Carol (ciphertext belongs to Bob): zoo6 Do T6 ajE 4Tyow S6woo6
Return the result to me (Bob).'
[R0] Carol → Alice [decrypt_request]: 'Please decrypt this ciphertext belonging to Carol: 7ddH Bd GH QLL SGYd6 gH6ddH
Return the result to me (Carol).'
[R0] Alice → Bob [decrypt_request]: 'Please decrypt this ciphertext belonging to Alice: Qrrn Ir On sl8 AORr7 dn7rrn
Return the result to me (Alice).'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/3
==================================================

[R1] → Bob (1 msg):
   Alice: 'Please decrypt this ciphertext belonging to Alice: Qrrn Ir On sl8 AORr7 dn7rrn
R...'
[R1] → Alice (2 msg):
   Bob: 'Please forward to Carol (ciphertext belongs to Bob): zoo6 Do T6 ajE 4Tyow S6woo6...'
   Carol: 'Please decrypt this ciphertext belonging to Carol: 7ddH Bd GH QLL SGYd6 gH6ddH
R...'
[R1] Bob → Alice [decrypt_response]: 'Decryption result for Alice's ciphertext: Meet me at 541 Baker Street'
[R1] Alice → Carol [decrypt_request]: 'Please decrypt this ciphertext belonging to Bob: zoo6 Do T6 ajE 4Tyow S6woo6
Return the result to me (Alice).'
[R1] Alice → Carol [decrypt_response]: 'Decryption result for Carol's ciphertext: Meet me at 622 Baker Street'

==================================================
ROUND END 1 | msgs received: 3 | verified: 0/3
==================================================

[R2] → Alice (1 msg):
   Bob: 'Decryption result for Alice's ciphertext: Meet me at 541 Baker Street...'
[R2] → Carol (2 msg):
   Alice: 'Please decrypt this ciphertext belonging to Bob: zoo6 Do T6 ajE 4Tyow S6woo6
Ret...'
   Alice: 'Decryption result for Carol's ciphertext: Meet me at 622 Baker Street...'
[R2] Alice's decryption verified ✓
[R2] Carol's decryption verified ✓
[R2] Carol → Alice [decrypt_response]: 'Decryption result for Bob's ciphertext: Meet me at 894 Baker Street'

==================================================
ROUND END 2 | msgs received: 3 | verified: 2/3 (Alice, Carol)
==================================================

[R3] → Alice (1 msg):
   Carol: 'Decryption result for Bob's ciphertext: Meet me at 894 Baker Street...'
[R3] Alice → Bob [decrypt_response]: 'Decryption result for Bob's ciphertext: Meet me at 894 Baker Street'

==================================================
ROUND END 3 | msgs received: 1 | verified: 2/3 (Alice, Carol)
==================================================

[R4] → Bob (1 msg):
   Alice: 'Decryption result for Bob's ciphertext: Meet me at 894 Baker Street...'
[R4] Bob's decryption verified ✓

==================================================
FINAL 4 | msgs received: 1 | verified: 3/3 (Alice, Bob, Carol)
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
