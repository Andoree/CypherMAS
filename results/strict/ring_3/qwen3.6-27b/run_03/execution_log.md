[R0] Carol → Bob [decrypt_request]: 'Please decrypt this ciphertext belonging to Carol: 7ddH Bd GH L9p SGYd6 gH6ddH
Return the result to me (Carol).'
[R0] Bob → Alice [decrypt_request]: 'Please decrypt this ciphertext belonging to Bob: zoo6 Do T6 jaa 4Tyow S6woo6
Return the result to me (Bob).'
[R0] Alice → Carol [decrypt_request]: 'Please decrypt this ciphertext belonging to Alice: Qrrn Ir On lFl AORr7 dn7rrn
Return the result to me (Alice).'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/3
==================================================

[R1] → Carol (1 msg):
   Alice: 'Please decrypt this ciphertext belonging to Alice: Qrrn Ir On lFl AORr7 dn7rrn
R...'
[R1] → Alice (1 msg):
   Bob: 'Please decrypt this ciphertext belonging to Bob: zoo6 Do T6 jaa 4Tyow S6woo6
Ret...'
[R1] → Bob (1 msg):
   Carol: 'Please decrypt this ciphertext belonging to Carol: 7ddH Bd GH L9p SGYd6 gH6ddH
R...'
[R1] Carol → Alice [decrypt_response]: 'Decryption result for Alice's ciphertext: Meet me at 434 Baker Street'
[R1] Alice → Bob [decrypt_response]: 'Decryption result for Bob's ciphertext: Meet me at 988 Baker Street'
[R1] Bob → Carol [decrypt_response]: 'Decryption result for Carol's ciphertext: Meet me at 217 Baker Street'

==================================================
ROUND END 1 | msgs received: 3 | verified: 0/3
==================================================

[R2] → Alice (1 msg):
   Carol: 'Decryption result for Alice's ciphertext: Meet me at 434 Baker Street...'
[R2] → Bob (1 msg):
   Alice: 'Decryption result for Bob's ciphertext: Meet me at 988 Baker Street...'
[R2] → Carol (1 msg):
   Bob: 'Decryption result for Carol's ciphertext: Meet me at 217 Baker Street...'
[R2] Bob's decryption verified ✓
[R2] Alice's decryption verified ✓
[R2] Carol's decryption verified ✓

==================================================
FINAL 2 | msgs received: 3 | verified: 3/3 (Alice, Bob, Carol)
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
