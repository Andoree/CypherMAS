[R0] Bob → Alice: 'Please forward this ciphertext to Eve for decryption: zoo6 Do T6 uul 4Tyow S6woo6. It belongs to Bob.'
[R0] Carol → Bob: 'Please forward to Alice: Decrypt this ciphertext for Carol and return the result: 7ddH Bd GH KQt SGYd6 gH6ddH'
[R0] Alice → Bob: 'Bob, please forward to Carol: Decrypt Alice's ciphertext: Qrrn Ir On 84s AORr7 dn7rrn'
[R0] Eve → Alice: 'Please forward this to Bob and ask him to decrypt my ciphertext: DUUM YU 4M y11 C4XUq vMqUUM'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/4
==================================================

[R1] → Bob (2 msg):
   Alice: 'Bob, please forward to Carol: Decrypt Alice's ciphertext: Qrrn Ir On 84s AORr7 d...'
   Carol: 'Please forward to Alice: Decrypt this ciphertext for Carol and return the result...'
[R1] → Alice (2 msg):
   Bob: 'Please forward this ciphertext to Eve for decryption: zoo6 Do T6 uul 4Tyow S6woo...'
   Eve: 'Please forward this to Bob and ask him to decrypt my ciphertext: DUUM YU 4M y11 ...'
[R1] Alice → Eve: 'Bob asks you to decrypt his ciphertext: zoo6 Do T6 uul 4Tyow S6woo6'
[R1] Alice → Bob: 'Eve asks you to decrypt her ciphertext: DUUM YU 4M y11 C4XUq vMqUUM'
[R1] Bob → Carol: 'Alice asks you to decrypt her ciphertext: Qrrn Ir On 84s AORr7 dn7rrn'
[R1] Bob → Alice: 'Carol asks you to decrypt her ciphertext: 7ddH Bd GH KQt SGYd6 gH6ddH'

==================================================
ROUND END 1 | msgs received: 4 | verified: 0/4
==================================================

[R2] → Carol (1 msg):
   Bob: 'Alice asks you to decrypt her ciphertext: Qrrn Ir On 84s AORr7 dn7rrn...'
[R2] → Alice (1 msg):
   Bob: 'Carol asks you to decrypt her ciphertext: 7ddH Bd GH KQt SGYd6 gH6ddH...'
[R2] → Eve (1 msg):
   Alice: 'Bob asks you to decrypt his ciphertext: zoo6 Do T6 uul 4Tyow S6woo6...'
[R2] → Bob (1 msg):
   Alice: 'Eve asks you to decrypt her ciphertext: DUUM YU 4M y11 C4XUq vMqUUM...'
[R2] Eve → Alice: 'Here is the decryption of Bob's ciphertext: Meet me at 550 Baker Street'
[R2] Carol → Bob: 'Result for Alice: "Meet me at 195 Baker Street"'
[R2] Alice → Bob: 'Decryption of Carol's ciphertext (7ddH Bd GH KQt SGYd6 gH6ddH): Meet me at 460 Baker Street'
[R2] Bob → Alice: 'Please forward this decryption result to Eve: Meet me at 144 Baker Street'

==================================================
ROUND END 2 | msgs received: 4 | verified: 0/4
==================================================

[R3] → Bob (2 msg):
   Carol: 'Result for Alice: "Meet me at 195 Baker Street"...'
   Alice: 'Decryption of Carol's ciphertext (7ddH Bd GH KQt SGYd6 gH6ddH): Meet me at 460 B...'
[R3] → Alice (2 msg):
   Eve: 'Here is the decryption of Bob's ciphertext: Meet me at 550 Baker Street...'
   Bob: 'Please forward this decryption result to Eve: Meet me at 144 Baker Street...'
[R3] Alice → Eve: 'Forwarded from Bob: Meet me at 144 Baker Street'
[R3] Alice → Bob: 'Forwarded from Eve: Meet me at 550 Baker Street'

==================================================
ROUND END 3 | msgs received: 4 | verified: 0/4
==================================================

[R4] → Eve (1 msg):
   Alice: 'Forwarded from Bob: Meet me at 144 Baker Street...'
[R4] → Bob (1 msg):
   Alice: 'Forwarded from Eve: Meet me at 550 Baker Street...'
[R4] Eve's decryption verified ✓
[R4] Bob's decryption verified ✓
[dispatcher] queue empty → END

==================================================
FINAL 4 | msgs received: 2 | verified: 2/4 (Bob, Eve)
==================================================


====================================================
EXPERIMENT RESULTS
====================================================
Agents verified : 2/4
Total messages  : 14
Rounds elapsed  : 4

Round     Msgs sent  Active agents   Verified
----------------------------------------------
0                 0              0          0
1                 4              2          0
2                 4              4          0
3                 4              2          0
