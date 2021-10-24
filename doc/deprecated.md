Functionalities:

| Name                    | Input                                      | Output                           |  
|-------------------------|--------------------------------------------|----------------------------------|    
| ZIP32 keygen            | `secret`, `i`                              | `sk`                             |  
| Key components gen      | `sk`                                       | `ask`, `fvk`, `ivk`, `ovk`, `dk` |  
| Address diversifier     | `dk`, `ivk`, `index`                       | `addr`                           |  
| Action shielder         | `action_plain`, `rseed`,`aplha`,`rcv`      | `action_shielded`                |  
| Note decryption via ivk | `ivk`, `epk`, `C_enc`                      | `note_plain` or failture         |  
| Note decryption via ovk | `ovk`, `epk`, `C_out`, `C_enc`, `cm`, `cv` | `note_plain`                     |
| Nullifier gen           | `nk`, `rseed`, `cm`, `nf_old`              | `nf_new`                         |  
| Spend signer            | `SIGHASH`, `ask`, `alpha`                  | `spendAuthSig`                   |  
| Binding signer          | `SIGHASH`, `rcv[]`, `cv_net`               | `bindingSig`                     |  
| Prover                  | `action_plain[]`, `action_shielded[]`, `fvk`, `alpha[]`, `rcv[]`, `rssed[]`, `cv_net`  | `proof` |