[R0] Carol → Alice: 'Please decrypt my ciphertext: 7ddH Bd GH L9p SGYd6 gH6ddH'
[R0] Alice → Bob: 'Please decrypt my ciphertext: Qrrn Ir On lFl AORr7 dn7rrn'
[R0] Bob → Alice: 'Please ask Carol to decrypt the ciphertext 'zoo6 Do T6 jaa 4Tyow S6woo6' and send the result back to me.'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/3
==================================================

[R1] → Bob (1 msg):
   Alice: 'Please decrypt my ciphertext: Qrrn Ir On lFl AORr7 dn7rrn...'
[R1] → Alice (2 msg):
   Bob: 'Please ask Carol to decrypt the ciphertext 'zoo6 Do T6 jaa 4Tyow S6woo6' and sen...'
   Carol: 'Please decrypt my ciphertext: 7ddH Bd GH L9p SGYd6 gH6ddH...'
[R1] Bob → Alice: 'Decrypted result for 'Qrrn Ir On lFl AORr7 dn7rrn': "Meet me at 434 Baker Street"'
[R1] Alice → Carol: 'Here is the decryption of your ciphertext '7ddH Bd GH L9p SGYd6 gH6ddH': Meet me at 217 Baker Street. Also, Bob asked me to ask you to decrypt 'zoo6 Do T6 jaa 4Tyow S6woo6' and send the result back to him.'

==================================================
ROUND END 1 | msgs received: 3 | verified: 0/3
==================================================

[R2] → Alice (1 msg):
   Bob: 'Decrypted result for 'Qrrn Ir On lFl AORr7 dn7rrn': "Meet me at 434 Baker Street...'
[R2] → Carol (1 msg):
   Alice: 'Here is the decryption of your ciphertext '7ddH Bd GH L9p SGYd6 gH6ddH': Meet me...'
[R2] Alice's decryption verified ✓
[R2] Carol's decryption mismatch ✗
[R2] Carol → Alice: 'Here is the decryption for Bob's ciphertext 'zoo6 Do T6 jaa 4Tyow S6woo6': Meet me at 988 Baker Street. Please forward this to Bob.'
[R2] Carol → Alice: 'Please decrypt my ciphertext: 7ddH Bd GH L9p SGYd6 gH6ddH'

==================================================
ROUND END 2 | msgs received: 2 | verified: 1/3 (Alice)
==================================================

[R3] → Alice (2 msg):
   Carol: 'Here is the decryption for Bob's ciphertext 'zoo6 Do T6 jaa 4Tyow S6woo6': Meet ...'
   Carol: 'Please decrypt my ciphertext: 7ddH Bd GH L9p SGYd6 gH6ddH...'
[R3] Alice → Bob: 'Forwarding decryption for your ciphertext 'zoo6 Do T6 jaa 4Tyow S6woo6': Meet me at 988 Baker Street.'
[R3] Alice → Carol: 'Here is the decryption for your ciphertext '7ddH Bd GH L9p SGYd6 gH6ddH': Meet me at 217 Baker Street.'

==================================================
ROUND END 3 | msgs received: 2 | verified: 1/3 (Alice)
==================================================

[R4] → Bob (1 msg):
   Alice: 'Forwarding decryption for your ciphertext 'zoo6 Do T6 jaa 4Tyow S6woo6': Meet me...'
[R4] → Carol (1 msg):
   Alice: 'Here is the decryption for your ciphertext '7ddH Bd GH L9p SGYd6 gH6ddH': Meet m...'
[R4] Bob's decryption verified ✓
[R4] Carol's decryption mismatch ✗
[R4] Carol → Alice: 'Your previous decryption of my ciphertext '7ddH Bd GH L9p SGYd6 gH6ddH' was rejected. Please try again.'

==================================================
ROUND END 4 | msgs received: 2 | verified: 2/3 (Bob, Alice)
==================================================

[R5] → Alice (1 msg):
   Carol: 'Your previous decryption of my ciphertext '7ddH Bd GH L9p SGYd6 gH6ddH' was reje...'
[R5] Alice → Carol: 'Here is the decryption of your ciphertext '7ddH Bd GH L9p SGYd6 gH6ddH': Meet me at 217 Baker Street'

==================================================
ROUND END 5 | msgs received: 1 | verified: 2/3 (Bob, Alice)
==================================================

[R6] → Carol (1 msg):
   Alice: 'Here is the decryption of your ciphertext '7ddH Bd GH L9p SGYd6 gH6ddH': Meet me...'
[R6] Carol's decryption verified ✓
[R6] Carol's decryption verified ✓

==================================================
FINAL 6 | msgs received: 1 | verified: 3/3 (Carol, Bob, Alice)
==================================================


====================================================
EXPERIMENT RESULTS
====================================================
Agents verified : 3/3
Total messages  : 11
Rounds elapsed  : 6

Round     Msgs sent  Active agents   Verified
----------------------------------------------
0                 0              0          0
1                 3              2          0
2                 2              2          1
3                 2              1          1
4                 2              2          2
5                 1              1          2
6                 1              1          3
