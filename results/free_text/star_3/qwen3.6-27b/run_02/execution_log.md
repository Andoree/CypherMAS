[R0] Carol → Alice: 'Please decrypt my ciphertext: 7ddH Bd GH QLL SGYd6 gH6ddH'
[R0] Alice → Bob: 'Please decrypt my ciphertext: Qrrn Ir On sl8 AORr7 dn7rrn'
[R0] Bob → Alice: 'Ciphertext: zoo6 Do T6 ajE 4Tyow S6woo6. Owner: Bob. Action: Please forward to Carol and ask her to decrypt it. Return the result to Bob.'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/3
==================================================

[R1] → Bob (1 msg):
   Alice: 'Please decrypt my ciphertext: Qrrn Ir On sl8 AORr7 dn7rrn...'
[R1] → Alice (2 msg):
   Bob: 'Ciphertext: zoo6 Do T6 ajE 4Tyow S6woo6. Owner: Bob. Action: Please forward to C...'
   Carol: 'Please decrypt my ciphertext: 7ddH Bd GH QLL SGYd6 gH6ddH...'
[R1] Bob → Alice: 'Decryption result for Qrrn Ir On sl8 AORr7 dn7rrn: Meet me at 541 Baker Street'

==================================================
ROUND END 1 | msgs received: 3 | verified: 0/3
==================================================

[R2] → Alice (1 msg):
   Bob: 'Decryption result for Qrrn Ir On sl8 AORr7 dn7rrn: Meet me at 541 Baker Street...'
[R2] Alice's decryption verified ✓
[R2] Alice → Carol: 'Your decryption result: Meet me at 622 Baker Street. Also, forwarding a request from Bob: Please decrypt ciphertext zoo6 Do T6 ajE 4Tyow S6woo6 (owned by Bob) and return the result to me so I can forward it to Bob.'

==================================================
ROUND END 2 | msgs received: 1 | verified: 1/3 (Alice)
==================================================

[R3] → Carol (1 msg):
   Alice: 'Your decryption result: Meet me at 622 Baker Street. Also, forwarding a request ...'
[R3] Carol's decryption mismatch ✗
[R3] Carol → Alice: 'Decryption of Bob's ciphertext 'zoo6 Do T6 ajE 4Tyow S6woo6' is 'Meet me at 894 Baker Street'. Please forward this to Bob.'
[R3] Carol → Alice: 'Please decrypt my ciphertext: 7ddH Bd GH QLL SGYd6 gH6ddH'

==================================================
ROUND END 3 | msgs received: 1 | verified: 1/3 (Alice)
==================================================

[R4] → Alice (2 msg):
   Carol: 'Decryption of Bob's ciphertext 'zoo6 Do T6 ajE 4Tyow S6woo6' is 'Meet me at 894 ...'
   Carol: 'Please decrypt my ciphertext: 7ddH Bd GH QLL SGYd6 gH6ddH...'
[R4] Alice → Carol: 'Your decryption result: Meet me at 622 Baker Street'
[R4] Alice → Bob: 'Decryption result for your ciphertext 'zoo6 Do T6 ajE 4Tyow S6woo6': Meet me at 894 Baker Street'

==================================================
ROUND END 4 | msgs received: 2 | verified: 1/3 (Alice)
==================================================

[R5] → Carol (1 msg):
   Alice: 'Your decryption result: Meet me at 622 Baker Street...'
[R5] → Bob (1 msg):
   Alice: 'Decryption result for your ciphertext 'zoo6 Do T6 ajE 4Tyow S6woo6': Meet me at ...'
[R5] Bob's decryption verified ✓
[R5] Carol's decryption verified ✓

==================================================
FINAL 5 | msgs received: 2 | verified: 3/3 (Carol, Bob, Alice)
==================================================


====================================================
EXPERIMENT RESULTS
====================================================
Agents verified : 3/3
Total messages  : 9
Rounds elapsed  : 5

Round     Msgs sent  Active agents   Verified
----------------------------------------------
0                 0              0          0
1                 3              2          0
2                 1              1          1
3                 1              1          1
4                 2              1          1
5                 2              2          3
