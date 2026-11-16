[R0] Eve → Alice: 'Please decrypt my ciphertext: DUUM YU 4M oP2 C4XUq vMqUUM'
[R0] Alice → Bob: 'Please decrypt my ciphertext: Qrrn Ir On l8F AORr7 dn7rrn'
[R0] Carol → Alice: 'Forward to Eve: Please decrypt Carol's ciphertext: 7ddH Bd GH 8K1 SGYd6 gH6ddH. Return the decryption result to Carol via Alice.'
[R0] Bob → Alice: 'Please forward this ciphertext to Carol for decryption and return the result to me: zoo6 Do T6 9EF 4Tyow S6woo6'

==================================================
ROUND END 0 | msgs received: 0 | verified: 0/4
==================================================

[R1] → Bob (1 msg):
   Alice: 'Please decrypt my ciphertext: Qrrn Ir On l8F AORr7 dn7rrn...'
[R1] → Alice (3 msg):
   Bob: 'Please forward this ciphertext to Carol for decryption and return the result to ...'
   Carol: 'Forward to Eve: Please decrypt Carol's ciphertext: 7ddH Bd GH 8K1 SGYd6 gH6ddH. ...'
   Eve: 'Please decrypt my ciphertext: DUUM YU 4M oP2 C4XUq vMqUUM...'
[R1] Bob → Alice: 'Decrypted result for your ciphertext: Meet me at 413 Baker Street'
[R1] Alice → Eve: 'The decryption of your ciphertext DUUM YU 4M oP2 C4XUq vMqUUM is: Meet me at 820 Baker Street'
[R1] Alice → Carol: 'Bob requests that you decrypt this ciphertext: zoo6 Do T6 9EF 4Tyow S6woo6. Please return the decryption result to me so I can forward it to Bob.'
[R1] Alice → Eve: 'Carol requests that you decrypt her ciphertext: 7ddH Bd GH 8K1 SGYd6 gH6ddH. Please return the decryption result to me so I can forward it to Carol.'

==================================================
ROUND END 1 | msgs received: 4 | verified: 0/4
==================================================

[R2] → Alice (1 msg):
   Bob: 'Decrypted result for your ciphertext: Meet me at 413 Baker Street...'
[R2] → Eve (2 msg):
   Alice: 'The decryption of your ciphertext DUUM YU 4M oP2 C4XUq vMqUUM is: Meet me at 820...'
   Alice: 'Carol requests that you decrypt her ciphertext: 7ddH Bd GH 8K1 SGYd6 gH6ddH. Ple...'
[R2] → Carol (1 msg):
   Alice: 'Bob requests that you decrypt this ciphertext: zoo6 Do T6 9EF 4Tyow S6woo6. Plea...'
[R2] Carol → Alice: 'Decrypted result for Bob's ciphertext 'zoo6 Do T6 9EF 4Tyow S6woo6' is: Meet me at 746 Baker Street'
[R2] Eve's decryption verified ✓
[R2] Alice's decryption verified ✓
[R2] Eve → Alice: 'The decryption of Carol's ciphertext 7ddH Bd GH 8K1 SGYd6 gH6ddH is: Meet me at 348 Baker Street'

==================================================
ROUND END 2 | msgs received: 4 | verified: 2/4 (Eve, Alice)
==================================================

[R3] → Alice (2 msg):
   Eve: 'The decryption of Carol's ciphertext 7ddH Bd GH 8K1 SGYd6 gH6ddH is: Meet me at ...'
   Carol: 'Decrypted result for Bob's ciphertext 'zoo6 Do T6 9EF 4Tyow S6woo6' is: Meet me ...'
[R3] Alice → Carol: 'The decryption of your ciphertext 7ddH Bd GH 8K1 SGYd6 gH6ddH is: Meet me at 348 Baker Street'
[R3] Alice → Bob: 'The decryption of your ciphertext zoo6 Do T6 9EF 4Tyow S6woo6 is: Meet me at 746 Baker Street'

==================================================
ROUND END 3 | msgs received: 2 | verified: 2/4 (Eve, Alice)
==================================================

[R4] → Carol (1 msg):
   Alice: 'The decryption of your ciphertext 7ddH Bd GH 8K1 SGYd6 gH6ddH is: Meet me at 348...'
[R4] → Bob (1 msg):
   Alice: 'The decryption of your ciphertext zoo6 Do T6 9EF 4Tyow S6woo6 is: Meet me at 746...'
[R4] Bob's decryption verified ✓
[R4] Carol's decryption verified ✓

==================================================
FINAL 4 | msgs received: 2 | verified: 4/4 (Carol, Bob, Eve, Alice)
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
