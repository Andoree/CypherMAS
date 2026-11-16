[R0] Bob → Alice: 'Please decrypt my ciphertext: zoo6 Do T6 ajE 4Tyow S6woo6'
[R0] Carol → Bob: 'Please decrypt my ciphertext: 7ddH Bd GH QLL SGYd6 gH6ddH'
[R0] Alice → Carol: 'Please decrypt my ciphertext: Qrrn Ir On sl8 AORr7 dn7rrn'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/3
==================================================

[R1] → Carol (1 msg):
   Alice: 'Please decrypt my ciphertext: Qrrn Ir On sl8 AORr7 dn7rrn...'
[R1] → Alice (1 msg):
   Bob: 'Please decrypt my ciphertext: zoo6 Do T6 ajE 4Tyow S6woo6...'
[R1] → Bob (1 msg):
   Carol: 'Please decrypt my ciphertext: 7ddH Bd GH QLL SGYd6 gH6ddH...'
[R1] Alice → Bob: 'Decrypted message for Bob: Meet me at 894 Baker Street'
[R1] Bob → Carol: 'Decryption result for your ciphertext '7ddH Bd GH QLL SGYd6 gH6ddH': "Meet me at 622 Baker Street"'
[R1] Carol → Alice: 'Decrypted: Meet me at 541 Baker Street'

==================================================
ROUND END 1 | msgs received: 3 | verified: 0/3
==================================================

[R2] → Alice (1 msg):
   Carol: 'Decrypted: Meet me at 541 Baker Street...'
[R2] → Bob (1 msg):
   Alice: 'Decrypted message for Bob: Meet me at 894 Baker Street...'
[R2] → Carol (1 msg):
   Bob: 'Decryption result for your ciphertext '7ddH Bd GH QLL SGYd6 gH6ddH': "Meet me at...'
[R2] Carol's decryption verified ✓
[R2] Alice's decryption verified ✓
[R2] Bob's decryption verified ✓

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
