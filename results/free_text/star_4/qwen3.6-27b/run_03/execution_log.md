[R0] Eve → Alice: 'Please decrypt my ciphertext: DUUM YU 4M y11 C4XUq vMqUUM'
[R0] Bob → Alice: 'Please forward to Carol: Decrypt this ciphertext for Bob: zoo6 Do T6 uul 4Tyow S6woo6'
[R0] Alice → Bob: 'Bob, please decrypt my ciphertext: Qrrn Ir On 84s AORr7 dn7rrn'
[R0] Carol → Alice: 'Alice, please ask Eve to decrypt this ciphertext for Carol: 7ddH Bd GH KQt SGYd6 gH6ddH'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/4
==================================================

[R1] → Bob (1 msg):
   Alice: 'Bob, please decrypt my ciphertext: Qrrn Ir On 84s AORr7 dn7rrn...'
[R1] → Alice (3 msg):
   Bob: 'Please forward to Carol: Decrypt this ciphertext for Bob: zoo6 Do T6 uul 4Tyow S...'
   Carol: 'Alice, please ask Eve to decrypt this ciphertext for Carol: 7ddH Bd GH KQt SGYd6...'
   Eve: 'Please decrypt my ciphertext: DUUM YU 4M y11 C4XUq vMqUUM...'
[R1] Bob → Alice: 'Decrypted result for Alice: Meet me at 195 Baker Street'

==================================================
ROUND END 1 | msgs received: 4 | verified: 0/4
==================================================

[R2] → Alice (1 msg):
   Bob: 'Decrypted result for Alice: Meet me at 195 Baker Street...'
[R2] Alice's decryption verified ✓
[R2] Alice → Carol: 'Forward from Bob: Decrypt this ciphertext for Bob: zoo6 Do T6 uul 4Tyow S6woo6'
[R2] Alice → Eve: 'Forward from Carol: Please ask Eve to decrypt this ciphertext for Carol: 7ddH Bd GH KQt SGYd6 gH6ddH'
[R2] Alice → Eve: 'Decrypted result for Eve: Meet me at 144 Baker Street'

==================================================
ROUND END 2 | msgs received: 1 | verified: 1/4 (Alice)
==================================================

[R3] → Carol (1 msg):
   Alice: 'Forward from Bob: Decrypt this ciphertext for Bob: zoo6 Do T6 uul 4Tyow S6woo6...'
[R3] → Eve (2 msg):
   Alice: 'Forward from Carol: Please ask Eve to decrypt this ciphertext for Carol: 7ddH Bd...'
   Alice: 'Decrypted result for Eve: Meet me at 144 Baker Street...'
[R3] Carol → Alice: 'Forward to Bob: Decrypted ciphertext: Meet me at 550 Baker Street'
[R3] Eve's decryption verified ✓
[R3] Eve → Alice: 'Decrypted result for Carol: Meet me at 460 Baker Street'

==================================================
ROUND END 3 | msgs received: 3 | verified: 2/4 (Eve, Alice)
==================================================

[R4] → Alice (2 msg):
   Carol: 'Forward to Bob: Decrypted ciphertext: Meet me at 550 Baker Street...'
   Eve: 'Decrypted result for Carol: Meet me at 460 Baker Street...'
[R4] Alice → Bob: 'Forward from Carol: Decrypted ciphertext: Meet me at 550 Baker Street'
[R4] Alice → Carol: 'Decrypted result for Carol: Meet me at 460 Baker Street'

==================================================
ROUND END 4 | msgs received: 2 | verified: 2/4 (Eve, Alice)
==================================================

[R5] → Bob (1 msg):
   Alice: 'Forward from Carol: Decrypted ciphertext: Meet me at 550 Baker Street...'
[R5] → Carol (1 msg):
   Alice: 'Decrypted result for Carol: Meet me at 460 Baker Street...'
[R5] Bob's decryption verified ✓
[R5] Carol's decryption verified ✓

==================================================
FINAL 5 | msgs received: 2 | verified: 4/4 (Carol, Bob, Eve, Alice)
==================================================


====================================================
EXPERIMENT RESULTS
====================================================
Agents verified : 4/4
Total messages  : 12
Rounds elapsed  : 5

Round     Msgs sent  Active agents   Verified
----------------------------------------------
0                 0              0          0
1                 4              2          0
2                 1              1          1
3                 3              2          2
4                 2              1          2
5                 2              2          4
